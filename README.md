<h1 align="center">Seizmeia</h1>

<div align="center">
<p>A credit management tool for a beer tap</p>
</div>

## Getting Started

Clone the repository:

```bash
git clone https://github.com/seizmeia/seizmeia.git
```

### Setup environment

Make sure you have `tox` installed in your system python and:

```bash
make env
```

### Run locally

Run:

```bash
make run
```

### Run with Docker Compose

To run the application:

```bash
make bup
```

To see it work:

```bash
curl localhost:8000
```

The application will autoreload on `/seizmeia` changes.

To stop the application:

```bash
make down
```
