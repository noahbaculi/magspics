<div id="top"></div>

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://magspics.com/">
    <img src="images/icons/favicon.png" alt="Logo" width="80" height="80">
  </a>

<h2 align="center">Mags Pics</h2>

<p align="center">
    Maggie Photography Portfolio
    <br />
    <a href="https://magspics.com/"><strong>Explore »</strong></a>
    <br />
    <br />
    <a href="https://github.com/noahbaculi/magspics/issues">Report Bug</a>
  </p>
</div>

<br />

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#development-workflow">Development Workflow</a></li>
  </ol>
</details>

<br>

<!-- ABOUT THE PROJECT -->

## About The Project

<br>
<p align="center">
  Just a little birthday present for my friend Mags to showcase her photography.
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- All relevant concepts, trademarks, copyright, and other intellectual property
  was utilized for personal use on behalf of Margaret Gutierrez.

<p align="right">(<a href="#top">back to top</a>)</p>

## Development Workflow

Install tools:

```shell
mise install
```

Run live server:

```shell
bunx live-server
```

Run image generator script:

```shell
uv run python ./images/image_generator.py
```

Check for broken links with [Lychee](https://github.com/lycheeverse/lychee):

```shell
lychee --root-dir . --cache .
```

