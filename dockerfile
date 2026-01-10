FROM ubuntu:24.04 AS builder
LABEL org.opencontainers.image.title="Pyaket"
LABEL org.opencontainers.image.description="📦 Easy Python to Fast Executables"
LABEL org.opencontainers.image.source="https://github.com/BrokenSource/Pyaket"
LABEL org.opencontainers.image.url="https://github.com/orgs/BrokenSource/packages"
LABEL org.opencontainers.image.documentation="https://pyaket.dev/"
LABEL org.opencontainers.image.authors="Tremeschin"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt update
WORKDIR "/app"

# Rust toolchain and common targets
RUN apt install -y curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"
RUN rustup default stable
RUN rustup target add x86_64-pc-windows-gnu
RUN rustup target add x86_64-unknown-linux-gnu
RUN rustup target add x86_64-apple-darwin
RUN rustup target add aarch64-pc-windows-gnullvm
RUN rustup target add aarch64-unknown-linux-gnu
RUN rustup target add aarch64-apple-darwin

# Install MacOS SDKs for cargo-zigbuild
RUN apt install -y xz-utils
RUN curl -L "https://github.com/phracker/MacOSX-SDKs/releases/download/11.3/MacOSX10.9.sdk.tar.xz" | tar -Jx -C /opt
RUN curl -L "https://github.com/phracker/MacOSX-SDKs/releases/download/11.3/MacOSX11.3.sdk.tar.xz" | tar -Jx -C /opt
ENV SDKROOT=/opt/MacOSX11.3.sdk

# Install astral-sh/uv, create ensure venv on path
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"
ENV UV_LINK_MODE="copy"
RUN uv venv "$VIRTUAL_ENV"

# Fixme: Builder for pyaket wheel avoid copying
# Copy and install pyaket[all] into venv
COPY . /app
RUN uv pip install .[all]
