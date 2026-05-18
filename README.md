# Startup Blueprint

A small Python web app that generates a five-year startup plan from two inputs:

- `industry`
- `country`

The app produces:

- Recommended org structure
- Headcount by year
- Expected annual revenue
- Expected annual operating costs
- Estimated annual funding required
- Per-person designations
- Annual salaries for each seat
- Salary explanations for each seat

## Requirements

- Python 3.11 or newer
- `pip`

## Run locally

1. Open a terminal in the repository.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it.

On PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Command Prompt:

```bat
.\.venv\Scripts\activate.bat
```

4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Start the server:

```bash
python app.py
```

6. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## How to use

1. Enter an `industry` such as `saas`, `fintech`, `healthtech`, `ecommerce`, `manufacturing`, or `consulting`.
2. Enter a `country` such as `United States`, `India`, `Germany`, or `Singapore`.
3. Click `Generate blueprint`.
4. Review the five-year financial plan, org structure, and employee salary rationale.

## Notes

- Figures are annual USD-equivalent planning estimates.
- Country input adjusts labor, overhead, facilities, and market scale.
- Industry input changes staffing mix, compliance intensity, margin profile, and revenue ramp.
