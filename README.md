<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=Data+engineer+-%3E+ML+infrastructure;Training+a+1B+model+from+scratch;Where+do+the+training+FLOPs+go%3F">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=0969DA&center=true&vCenter=true&width=600&lines=Data+engineer+-%3E+ML+infrastructure;Training+a+1B+model+from+scratch;Where+do+the+training+FLOPs+go%3F" alt="Data engineer moving into ML infrastructure" />
  </picture>
</div>

```text
╔═════════════════════════════════════════════════════════════════╗
║  almaz@amsterdam:~$ whoami                                      ║
║                                                                 ║
║  Senior data engineer at Xebia, 10+ years of pipelines on GCP.  ║
║  Now on the other side of them: training and serving LLMs.      ║
║                                                                 ║
║  status: training | measuring | writing it down                 ║
╚═════════════════════════════════════════════════════════════════╝
```

## What I'm building

- **A language model from scratch.** 1.04B parameters, 20B tokens of FineWeb-Edu, my own tokenizer and training loop. The 100M dry-run is done, the main run is next.
- **[TrainMeter](https://pypi.org/project/trainmeter/)** - where the training FLOPs go and how well the GPUs are used. MFU measured on the run, not assumed from a spec sheet.
- **Stanford CS336, Spring 2026** - language modeling from scratch, worked through by hand: tokenizer, transformer, kernels, parallelism.
- **XKE sessions at Xebia** - a talk series for colleagues on how LLMs are built, trained and served.

```python
focus = {
    "now":     ["pretraining", "MFU and FLOP accounting", "distributed PyTorch"],
    "next":    ["inference as a storage hierarchy", "KV cache tiering"],
    "day job": ["BigQuery", "dbt", "Terraform", "Cloud Composer"],
}
```

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=python%2Crust%2Cpytorch%2Cgcp%2Cterraform%2Cdocker%2Ckubernetes%2Clinux%2Cpostgres%2Cfastapi%2Creact%2Cts%2Cgit%2Cgithubactions&theme=dark">
    <img src="https://skillicons.dev/icons?i=python%2Crust%2Cpytorch%2Cgcp%2Cterraform%2Cdocker%2Ckubernetes%2Clinux%2Cpostgres%2Cfastapi%2Creact%2Cts%2Cgit%2Cgithubactions&theme=light" alt="Python, Rust, PyTorch, GCP, Terraform, Docker, Kubernetes, Linux, Postgres, FastAPI, React, TypeScript, Git, GitHub Actions" />
  </picture>
</div>

## Elsewhere

- [almaz.murzabekov.net](https://almaz.murzabekov.net) - notes on what broke, with the numbers behind it.
- [nookat](https://github.com/nookat-io/nookat) - a lightweight container manager in Tauri, Rust and React.
- [one-billion-row-challenge](https://github.com/Almaz-KG/one-billion-row-challenge) - 1BRC implementations in different languages.

If you are working on the same seam between data engineering and ML infrastructure, open an issue on any of these repos. I read them.
