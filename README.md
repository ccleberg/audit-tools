# Audit Tools

**Audit Tools** is a collection of open-source Python scripts and related resources intended to support auditors, risk professionals, and data analysts in automating common audit procedures and analyses.

This repository includes practical examples that can be used as-is or adapted to specific audit environments.

## Contents

The repository includes scripts and templates related to:

- Pseudo-random sampling
- General IT controls (GITC) extraction and analysis
- Project management tracking and visualization
- Cloud platform analysis (planned)
- Prompt engineering and AI audit guidance (planned)

These tools are intended to be straightforward and applicable across a range of audit contexts.

## Getting Started

**Clone the Repository**

```bash
git clone https://github.com/audit-labs/audit-tools
cd audit-tools
```

**Install Dependencies**

Required for running the Python scripts:

```bash
pip install -r requirements.txt

# or, if you prefer `uv`:
uv run file.py
```

**Run a Sample Script**

For example, to run the Linux OS report tool:

```bash
./os/linux/report/linux.sh
```

Output will be shown in the terminal or saved to a file, depending on the script.

## Resources

If you're new to scripting or audit analytics, you may find the following helpful:

- [Python for Auditors](https://realpython.com)
- [Audit Analytics 101](https://audit-analytics.com)
- [Getting Started with Pandas](https://pandas.pydata.org/docs/getting_started/)

See the `notebooks/` directory for additional walkthroughs and examples.

## Contributing

Contributions are welcome. You can contribute by:

- Adding new audit-related scripts
- Suggesting improvements or feature ideas
- Enhancing documentation or tutorials
- Testing the tools on additional datasets and reporting any issues

To contribute:

1. Fork the repository
2. Create a new branch:

   ```bash
   git checkout -b my-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m 'Added new audit test'
   ```

4. Push your branch:

   ```bash
   git push origin my-feature
   ```

5. Open a pull request
