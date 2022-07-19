import uvicorn

from family_tree_backend.controller import api
from family_tree_backend.model.family_tree import FamilyTree


ft = FamilyTree()


def main():
    uvicorn.run(api.app, host="127.0.0.1", port=8080)


if __name__ == '__main__':
    main()
