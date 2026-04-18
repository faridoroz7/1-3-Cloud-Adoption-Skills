# Karmada K8s Switch Skill

This skill package provides a verified Karmada-based Kubernetes cluster switching PoC for a local lab environment. It covers host preparation, Karmada bootstrap, deployment of a stateless failover demo across `member1` and `member2`, traffic cutover through a stable host endpoint, and environment teardown.

## Included Assets

- [SKILL.md](./SKILL.md): Main skill definition, trigger conditions, workflow, and validation gates
- [references/](./references): Host preparation, Karmada bootstrap, and failover PoC procedures
- [agents/](./agents): Agent metadata for skill invocation

## Typical Use

- Prepare a local Karmada lab on a single Linux host
- Deploy the proven `member1` and `member2` stateless failover PoC
- Trigger failover from `cluster 1` to `cluster 2`
- Validate cutover behavior through one fixed browser endpoint
- Clean up the Karmada and kind environment after testing
