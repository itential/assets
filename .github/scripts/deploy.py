#!/usr/bin/env python3
"""
Deployment script for promoting Itential assets using asyncplatform.

This script reads asset files from the repository and imports them into
the target Itential Platform environment using the asyncplatform library.

Currently supports:
    - Studio projects
    - Operations Manager automations
    - Lifecycle Manager resources
    - Configuration Manager golden configs

Usage:
    python deploy.py <environment>

Required environment variables:
    HOST              - Itential Platform hostname
    CLIENT_ID         - OAuth service account client ID
    CLIENT_SECRET     - OAuth service account client secret
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import asyncplatform
from asyncplatform.models.projects import ProjectMember

class AssetDeployer:
    """Handles deployment of Itential assets to a target environment."""

    def __init__(self, environment: str, members: list[dict[str, str]] | None = None):
        """Initialize deployer with environment configuration.

        Args:
            environment: Target environment name
            members: Optional list of project members with username, type, and role
        """
        self.environment = environment
        self.members = members or []
        self.host = os.environ.get("HOST")
        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")

        if not all([self.host, self.client_id, self.client_secret]):
            raise ValueError(
                "Missing required environment variables: "
                "HOST, CLIENT_ID, CLIENT_SECRET"
            )

        print(f"🚀 Deploying to {environment} environment")

    # Maps each asset directory name (must match diff.sh's ASSET_DIRS) to the
    # bucket key, emoji, and label used when reporting found files.
    _ASSET_DIR_MAP = {
        "Studio Projects": ("projects", "📦", "Studio project"),
        "Automations": ("automations", "🤖", "automation"),
        "LCM Resource Models": ("lifecycle_manager_resources", "🔧", "LCM resource model"),
        "Golden Configs": ("configurations", "⚙️ ", "golden config"),
    }

    def find_asset_files(self) -> dict[str, list[Path]]:
        """Find asset files to deploy.

        If CHANGED_FILES env var is set (JSON array of repo-relative paths
        from diff.sh), those exact files are used directly — diff.sh already
        determined what changed, so no filesystem walk is needed. Otherwise,
        every asset file in the repo is found via a full glob (manual run).

        Returns:
            Dictionary mapping asset types to list of file paths
        """
        repo_root = Path.cwd()

        assets: dict[str, list[Path]] = {
            "projects": [],
            "automations": [],
            "lifecycle_manager_resources": [],
            "configurations": [],
        }

        changed_raw = os.environ.get("CHANGED_FILES", "")
        changed_files: list[str] | None = None
        if changed_raw:
            try:
                changed_files = json.loads(changed_raw)
            except json.JSONDecodeError:
                pass

        if changed_files is not None:
            for rel_path in changed_files:
                f = repo_root / rel_path
                mapping = self._ASSET_DIR_MAP.get(f.parent.name)
                if mapping is None:
                    continue
                bucket, emoji, label = mapping
                assets[bucket].append(f)
                print(f"{emoji} Found {label}: {f.name}")
            return assets

        # No CHANGED_FILES set — full-repo run, walk the tree.
        for dir_name, (bucket, emoji, label) in self._ASSET_DIR_MAP.items():
            for asset_dir in repo_root.glob(f"**/{dir_name}"):
                if asset_dir.is_dir():
                    for f in asset_dir.glob("*.json"):
                        assets[bucket].append(f)
                        print(f"{emoji} Found {label}: {f.name}")

        return assets

    async def deploy_projects(self, client: Any, project_files: list[Path]) -> None:
        """Deploy Studio projects to the platform.

        Args:
            client: Asyncplatform client instance
            project_files: List of project file paths
        """
        if not project_files:
            print("ℹ️  No Studio projects to deploy")
            return

        projects_resource = client.resource("projects")

        for project_file in project_files:
            with open(project_file, "r") as f:
                project_data = json.load(f)
            project_name = project_data.get("name", project_file.stem)

            try:
                print(f"📥 Importing project: {project_name}")

                # Convert members dict to ProjectMember objects
                # Support both schemas: account (username) and group (name)
                members = []
                for member in self.members:
                    member_data = {
                        "type": member["type"],
                        "role": member["role"]
                    }
                    # Use "username" for accounts, "name" for groups
                    if member["type"] == "account":
                        member_data["username"] = member["username"]
                    else:  # type == "group"
                        member_data["name"] = member["name"]

                    members.append(ProjectMember(**member_data))

                # Import project with members (overwrite if exists)
                result = await projects_resource.importer(
                    project_data,
                    members=members,
                    overwrite=True,
                    skip_reference_validation=True
                )
                print(f"✅ Successfully imported project: {result['name']}")
                if members:
                    for member in members:
                        member_identifier = (
                            getattr(member, 'username', None) or
                            getattr(member, 'name', 'unknown')
                        )
                        print(f"👤 Added {member.type} {member_identifier} as {member.role}")
            except Exception as e:
                print(f"❌ Failed to import project {project_name}: {e}")
                raise

    # async def deploy_agent_projects(
    #     self, client: Any, bundle_files: list[Path]
    # ) -> None:
    #     agent_projects_resource = client.resource("agent_projects")
    #     for bundle_file in bundle_files:
    #         with open(bundle_file, "r") as f:
    #             bundle_data = json.load(f)
    #         bundle_name = bundle_data.get("name", bundle_file.stem)
    #         try:
    #             members = []
    #             for member in self.members:
    #                 member_data = {"type": member["type"], "role": member["role"]}
    #                 if member["type"] == "account":
    #                     member_data["username"] = member["username"]
    #                 else:
    #                     member_data["name"] = member["name"]
    #                 members.append(ProjectMember(**member_data))
    #             await agent_projects_resource.importer(bundle_data, members=members)
    #             print(f"✅ Successfully imported Agent project: {bundle_name}")
    #         except Exception as e:
    #             print(f"❌ Failed to import Agent project {bundle_name}: {e}")
    #             raise

    async def deploy_automations(
        self, client: Any, automation_files: list[Path]
    ) -> None:
        """Deploy Operations Manager automations to the platform.

        Args:
            client: Asyncplatform client instance
            automation_files: List of automation file paths
        """
        if not automation_files:
            print("ℹ️  No automations to deploy")
            return

        automations_resource = client.resource("automations")

        for automation_file in automation_files:
            with open(automation_file, "r") as f:
                automation_data = json.load(f)
            automation_name = automation_data.get("name", automation_file.stem)

            try:
                existing_automation = await automations_resource.get_automation_by_name(
                    automation_name
                )

                if existing_automation:
                    print(f"ℹ️  Automation already exists, skipping: {automation_name}")
                    continue

                print(f"📥 Importing automation: {automation_name}")
                result = await automations_resource.importer(automation_data)
                print(f"✅ Successfully imported automation: {result['name']}")
            except Exception as e:
                print(f"❌ Failed to import automation {automation_name}: {e}")
                print(f"⚠️  Skipping {automation_name} and continuing deployment")
    
    async def deploy_lifecycle_manager_resources(
        self, client: Any, resource_files: list[Path]
    ) -> None:
        """Deploy Lifecycle Manager resource models to the platform.

        Args:
            client: Asyncplatform client instance
            resource_files: List of lifecycle manager resource file paths
        """
        if not resource_files:
            print("ℹ️  No Lifecycle Manager resources to deploy")
            return

        lm_resource = client.resource("lifecycle_manager")
        lifecyle_manager_resource_payload = {
            "model":{} 
            }
        for resource_file in resource_files:
            with open(resource_file, "r") as f:
                resource_data = json.load(f)
                lifecyle_manager_resource_payload["model"] = resource_data
            resource_name = resource_data.get("name", resource_file.name)
            
            try:
                existing_resource = await lm_resource.get_resource_by_name(resource_name)
                if existing_resource:
                    print(f"ℹ️  Resource model already exists, skipping: {resource_name}")
                    continue

                print(f"📥 Importing resource model: {resource_name}")
                result = await lm_resource.importer(lifecyle_manager_resource_payload)
                print(f"✅ Successfully imported resource model: {result['data']['name']}")
            except Exception as e:
                print(f"❌ Failed to import resource model {resource_name}: {e}")
                raise

    async def deploy_configurations(
        self, client: Any, config_files: list[Path]
    ) -> None:
        """Deploy Configuration Manager golden configs to the platform.

        Args:
            client: Asyncplatform client instance
            config_files: List of golden config file paths
        """
        if not config_files:
            print("ℹ️  No Configuration Manager golden configs to deploy")
            return

        cm_resource = client.resource("configuration_manager")

        for config_file in config_files:
            with open(config_file, "r") as f:
                config_data = json.load(f)
            config_name = config_data.get("data", [{}])[0].get("name", config_file.stem)

            try:
                if await cm_resource.check_if_golden_config_exists(config_name):
                    print(f"ℹ️  Golden config already exists, skipping: {config_name}")
                    continue

                print(f"📥 Importing golden config: {config_name}")
                result = await cm_resource.import_golden_config([config_data])
                print(f"✅ {result.get('message', f'Successfully imported golden config: {config_name}')}")
            except Exception as e:
                print(f"❌ Failed to import golden config {config_name}: {e}")
                raise

    async def deploy(self) -> None:
        """Execute the deployment process."""
        print(f"\n{'='*60}")
        print(f"Starting deployment to {self.environment}")
        print(f"{'='*60}\n")

        # Find all asset files
        assets = self.find_asset_files()

        if not any(assets.values()):
            print("⚠️  No assets found to deploy")
            return

        # Deploy assets via asyncplatform
        async with asyncplatform.client(
            host=self.host,
            client_id=self.client_id,
            client_secret=self.client_secret,
            verify=True,
        ) as client:
            print(f"\n✅ Connected to Itential Platform: {self.host}\n")

            await self.deploy_projects(client, assets["projects"])

            # await self.deploy_agent_projects(client, assets["agent_projects"])

            await self.deploy_lifecycle_manager_resources(
                client, assets["lifecycle_manager_resources"]
            )

            await self.deploy_automations(client, assets["automations"])

            await self.deploy_configurations(client, assets["configurations"])

        print(f"\n{'='*60}")
        print(f"✅ Deployment to {self.environment} completed successfully!")
        print(f"{'='*60}\n")


def main():
    """Main entry point for the deployment script."""
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]

    # Read members from environment variable (JSON array)
    members = []
    members_json = os.getenv("PROJECT_MEMBERS")
    if members_json:
        try:
            members = json.loads(members_json)
        except json.JSONDecodeError as e:
            print(f"⚠️  Invalid PROJECT_MEMBERS JSON: {e}")
            print("Continuing without project members")

    try:
        deployer = AssetDeployer(environment, members=members)
        asyncio.run(deployer.deploy())
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
