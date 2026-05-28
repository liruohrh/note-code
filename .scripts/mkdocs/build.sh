mkdir -p build/www/docs/
rsync -a \
--exclude='.git' \
--exclude='.github' \
--exclude='.makemd' \
--exclude='.obsidian' \
--exclude='.scripts' \
--exclude='.venv' \
--exclude='.vscode' \
--exclude='.zed' \
--exclude='.idea' \
--exclude='build' \
--exclude='mkdocs.yml' \
--exclude='README.md' \
. build/www/docs/
# mkdocs build --strict
mkdocs build
