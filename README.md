# Commiter

This project provides a small script for generating GitHub commits on selected days. When started it displays a calendar based on a user's previous contributions. You can mark squares with different activity levels (shades of green). The program then creates the corresponding number of commits for each chosen day and pushes them to the repository.

## Requirements

- Python 3.8 or newer
- Dependencies listed in `requiremnts.txt`

Install them with:
```bash
pip install -r requiremnts.txt
```


## Usage

```
python main.py
```

After launching, provide the year and GitHub user name. You can then mark days in the calendar. Clicking **Commit to GitHub** will perform the commits and push them to the `main` branch.

The file `file.txt` is only used as a temporary storage for commit contents.

## Warning

Using this tool rewrites repository history. Use it carefully.

## License

This project is licensed under the [MIT License](LICENSE).
