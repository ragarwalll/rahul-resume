FROM debian:bullseye-slim as builder

# Install required packages for downloading and extracting
RUN apt-get update && apt-get install -y \
    wget \
    perl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /tmp

# Download TeX Live installer
RUN wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz

# Extract the installer
RUN zcat < install-tl-unx.tar.gz | tar xf -

# Change to the installer directory and run installation
RUN cd install-tl-* && \
    perl ./install-tl --no-interaction --scheme=small

# Create final image
FROM debian:bullseye-slim

# Copy installed TeX Live from builder
COPY --from=builder /usr/local/texlive /usr/local/texlive

# Add TeX Live binaries to PATH
ENV PATH="/usr/local/texlive/2024/bin/aarch64-linux:${PATH}"

# Verify installation
RUN tlmgr --version

# Set working directory
WORKDIR /workspace

# Add a health check
HEALTHCHECK --interval=5m --timeout=3s \
  CMD pdflatex --version || exit 1