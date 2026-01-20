# Using debian for conservative glibc
FROM debian:bookworm-slim AS image
LABEL org.opencontainers.image.title="Pyaket"
LABEL org.opencontainers.image.description="📦 Easy Python to Fast Executables"
LABEL org.opencontainers.image.source="https://github.com/BrokenSource/Pyaket"
LABEL org.opencontainers.image.url="https://github.com/orgs/BrokenSource/packages"
LABEL org.opencontainers.image.documentation="https://pyaket.dev/"
LABEL org.opencontainers.image.authors="Tremeschin"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
WORKDIR "/app"

# Enable caching on docker apt..
RUN rm /etc/apt/apt.conf.d/docker-clean
RUN echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
    > /etc/apt/apt.conf.d/keep-cache

# So much clean commands wow
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update

# General tools, https, git, sdk unpacking..
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt install -y --no-install-recommends \
    build-essential ca-certificates curl git xz-utils

# Get and configure astral-sh/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_PYTHON_CACHE_DIR="/root/.cache/uv/python"
ENV UV_COMPILE_BYTECODE="1"
ENV UV_LINK_MODE="copy"

# Cache a python download
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install

# Make and activate a venv
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv

# Rust toolchain and common targets
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install rustbin
RUN uv run rustup set profile minimal
RUN uv run rustup default stable
RUN uv run rustup target add aarch64-apple-darwin
RUN uv run rustup target add aarch64-unknown-linux-gnu
RUN uv run rustup target add x86_64-apple-darwin
RUN uv run rustup target add x86_64-pc-windows-gnu
RUN uv run rustup target add x86_64-unknown-linux-gnu

# Install mingw for windows builds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt install -y --no-install-recommends \
    mingw-w64

# Install MacOS SDKs for cargo-zigbuild
RUN curl -L "https://github.com/phracker/MacOSX-SDKs/releases/download/11.3/MacOSX11.3.sdk.tar.xz" | tar -Jx -C /opt
ENV SDKROOT="/opt/MacOSX11.3.sdk"

# Fixme: Stinkingly works, but seems like a ziglang bug
# - https://github.com/ziglang/zig/issues/23179
# - https://github.com/rust-cross/cargo-zigbuild/issues/324
RUN ln -s $SDKROOT/System /System

# Note: Lazy and dislike copying or mounting local files
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install "git+https://github.com/BrokenSource/Pyaket#egg=pyaket[all]"

# Fetch and include locked crates
RUN cargo fetch --manifest-path $(find $VIRTUAL_ENV -path '*/pyaket/Cargo.toml')

# Fixme: Share artifacts without root ownership
# Fixme: Mount wheel directories in container
