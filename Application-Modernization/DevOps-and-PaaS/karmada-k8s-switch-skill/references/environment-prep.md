# Environment Preparation

Use this reference before bootstrapping or repairing the local Karmada lab.

## Scope

This PoC was proven on a single Linux host with:

- Docker available to root
- `kind`, `kubectl`, `go`, and `curl` in `PATH`
- writable `/root/.kube`
- enough inotify capacity for kind-based clusters

## Known Good PATH

Use this shell preamble before running repo scripts:

```bash
export PATH=/usr/local/go/bin:/root/go/bin:/root/.local/bin:$PATH
```

If `kind` is missing, check:

```bash
which kind
which kubectl
which go
docker version
```

## Inotify Fix for kind

This host needed higher inotify limits or CoreDNS and kube-proxy would become unstable. The proven persistent fix was:

`/etc/sysctl.d/99-karmada-kind.conf`

```conf
fs.inotify.max_user_instances = 8192
fs.inotify.max_user_watches = 1048576
```

Apply it with:

```bash
sysctl --system
```

Quick verification:

```bash
sysctl fs.inotify.max_user_instances
sysctl fs.inotify.max_user_watches
```

## Docker Health Check

Before bringing Karmada up:

```bash
systemctl is-active docker
docker ps
```

If Docker is not running, start it before doing anything else.

## Repo Location

The verified PoC assumes this repo path:

```bash
cd /root/karmada
```

The failover demo assets live in:

```bash
/root/karmada/samples/failover-demo
```

## Accuracy Rules

- Do not rewrite the bootstrap flow if the repo already has a tested script.
- Do not create alternate manifests when the existing ones match the PoC.
- If the host is already dirty, inspect current clusters and containers before creating new ones.
- If kubeconfigs are missing but kind containers exist, reconstruct state carefully instead of blindly redeploying.
