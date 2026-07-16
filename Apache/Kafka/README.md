Apache Kafka is a distributed event streaming platform used for publishing, subscribing to, and processing real-time data feeds across producers and consumers organized into topics.

This project provides a Studio Project built on the **Kafka Adapter** — a workflow to produce messages to a topic, and a workflow to consume messages, designed to be invoked by an Operations Manager event trigger. See **Studio Projects** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter](#adapter)
  - [Event Trigger (Consume Message)](#event-trigger-consume-message)
- [Studio Projects](#studio-projects)
  - [Apache Kafka 2.x Project](#apache-kafka-2x-project)

## Contents

| Asset | Description |
|---|---|
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the Produce Message and Consume Message workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Apache Kafka | 2.x brokers |
| Kafka Adapter | Required for both workflows below |

## Integration Configuration

### Adapter

Install the [Kafka Adapter](https://gitlab.com/itentialopensource/adapters/adapter-kafkav2) and configure an instance in **Admin > Adapters** pointing at your Kafka broker(s), then update the `adapterId` value in the Produce Message workflow to match your instance name before importing.

### Event Trigger (Consume Message)

The **Consume Message** workflow isn't meant to be run manually — it's designed to be invoked automatically whenever the Kafka Adapter emits a message event. This repo doesn't ship an exported Automation/Trigger for it (the topic name is tenant-specific), so wire it up manually after importing the Studio Project:

1. In **Operations Manager > Automations**, create a new Automation and set its workflow to **Consume Message** (from the imported Studio Project).
2. In **Operations Manager > Triggers**, create a new trigger with:
   - **Type**: Event
   - **Source**: `@itentialopensource/adapter-kafkav2` — matches your Kafka Adapter's package name
   - **Topic**: the Kafka topic you want to consume from (e.g. `example-topic`)
   - **Action Type**: Automations
   - **Action**: the Automation created in step 1
   - **Legacy Wrapper**: off/disabled
   - **Schema / JST**: leave both empty — with no transformation defined, the adapter's raw event data flows straight into the workflow's `payload` input variable
3. Enable the trigger. Every message the adapter receives on that topic now starts a **Consume Message** job with the message body available at `$var.job.payload`.

## Studio Projects

Import [`Apache Kafka 2.x.project.json`](./Studio%20Projects/Apache%20Kafka%202.x.project.json) via **Automation Studio > Projects > Import**.

### Apache Kafka 2.x Project

| Workflow | Scope |
|---|---|
| Produce Message | Publish one or more messages to a Kafka topic. Inputs: `adapterId`, `topic`, `messages` (array of message strings). Uses a **Build Produce Message Request** transformation internally to shape the adapter payload. |
| Consume Message | Receives a single message payload and processes it. Input: `payload` (object) — meant to be populated by the event trigger described above, not supplied manually. |

#### Dependencies

| Dependency | Notes |
|---|---|
| [Kafka Adapter](https://gitlab.com/itentialopensource/adapters/adapter-kafkav2) | Required for both workflows. Update `adapterId` in Produce Message, and reference the adapter's package name as the event source when configuring the trigger. |
