import sys

def main():
    if "--cli" in sys.argv:
        import cli
        cli.run()
    else:
        import gui
        gui.run()

if __name__ == "__main__":
    main()
