# Define a function named main.
# The -> None annotation says this function returns no meaningful value.
def main() -> None:
    # Store a string in a variable named project_name.
    project_name = "DocDesk"

    # Store another string describing our current learning milestone.
    milestone = "Project setup"

    # Print a message, inserting the variable's value into the string.
    print(f"Welcome to {project_name}!")

    # Print the milestone on a separate line.
    print(f"Current milestone: {milestone}")


# Run main() only when this file is executed directly.
# Importing this file from another module will not run main().
if __name__ == "__main__":
    main()