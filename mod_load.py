import importlib.util
import sys


def dynamic_import_from_file(module_name: str, file_path: str):
    """
    Dynamically imports a Python module from a specified file path.

    Args:
        module_name (str): The name to assign to the imported module.
        file_path (str): The full path to the Python file (.py) to import.

    Returns:
        module: The imported module object.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(
            f"Could not find module spec for {module_name} at {file_path}"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Add the module to sys.modules
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    module_name = "my_dynamic_module"
    file_path = "my_dynamic_module.py"  # Adjust path if needed

    try:
        # Dynamically import the module
        dynamic_module = dynamic_import_from_file(module_name, file_path)

        # Now you can use the imported module and its contents
        print(dynamic_module.greet("World"))
        my_instance = dynamic_module.MyClass(42)
        print(my_instance.get_value())

    except ImportError as e:
        print(f"Error importing module: {e}")
