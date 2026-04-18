---
name: karmada-k8s-switch-skill
description: Use when the user wants to prepare a local Karmada lab, install and verify the Karmada control plane, deploy the tested member1/member2 stateless failover PoC in /root/karmada, switch traffic between Kubernetes clusters, validate cutover behavior, or tear the environment down. This skill favors the repo's proven scripts and manifests over ad hoc setup so the PoC is faster and more accurate.
---

# Karmada K8s Switch Skill

## Overview

This skill drives the verified local Karmada failover PoC that was already implemented in `/root/karmada`. Default to the repo's bootstrap scripts, manifests, and demo helpers instead of inventing a new deployment flow.

## Use This Skill When

- The user wants a working Karmada environment on a single host.
- The user wants a stateless Kubernetes cluster switch demo with `member1` and `member2`.
- The user wants to prove failover or failback through a stable host entrypoint.
- The user wants cleanup of the local Karmada and kind environment.

## Default Workflow

1. Read [references/environment-prep.md](references/environment-prep.md) before changing the host.
2. Read [references/karmada-bootstrap.md](references/karmada-bootstrap.md) before bringing Karmada up or down.
3. Read [references/failover-demo-poc.md](references/failover-demo-poc.md) before deploying, switching, or validating the PoC.
4. Reuse the existing assets in `/root/karmada/samples/failover-demo` unless the user explicitly asks for a redesign.

## Operating Rules

- Prefer `hack/local-up-karmada.sh` for the first working environment. It is the fastest verified bootstrap in this repo.
- Accept that the standard bootstrap creates `member3`. For this PoC, use `member1` and `member2` and ignore `member3` unless the user explicitly asks for a two-member custom bootstrap.
- Prefer the host-side proxy in `/root/karmada/samples/failover-demo/scripts/start-proxy.sh` so the browser entrypoint stays fixed during cutover.
- Treat the demo as stateless. Do not describe it as state migration. The proof comes from successful probes, heartbeat continuity, and backend switch events.
- Do not claim "no interruption" unless the probe timeline and endpoint checks stayed healthy during the switch.
- When cleanup is requested, prefer `hack/local-down-karmada.sh`; if the environment is partially broken, fall back to explicit `kind delete cluster` commands.

## Fast Path

Use this order unless the user asks for a custom flow:

1. Prepare the host and verify Docker, `kind`, `kubectl`, and Go.
2. Run `hack/local-up-karmada.sh`.
3. Build and deploy `/root/karmada/samples/failover-demo`.
4. Start the host proxy and verify `http://127.0.0.1:8088/`.
5. Trigger failover to `member2` and validate the switch.
6. Converge Karmada placement to `member2` if the user wants migration completion.
7. Recover `member1` and fail back only if the user asks for that second step.

## Validation Gates

- Karmada control plane is reachable via `/root/.kube/karmada.config`.
- `kubectl --kubeconfig=/root/.kube/karmada.config --context=karmada-apiserver get clusters` shows `member1` and `member2` as ready.
- The demo app rolls out on both member clusters before traffic switching starts.
- `http://127.0.0.1:8088/status` clearly reports `cluster 1` or `cluster 2`.
- Direct member endpoints and the proxied endpoint agree with the intended traffic target.

## Deliverables

When reporting back to the user, include:

- what was installed or changed on the host
- which commands were run
- current cluster and proxy status
- whether traffic is on `cluster 1` or `cluster 2`
- any deviations from the verified PoC path
