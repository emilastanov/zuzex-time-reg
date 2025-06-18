import importlib
import os

from utils.log_answer import sync_sys_log


def load_module(app, module_dir, func, named=False, pattern=None, filters=False):

    command_modules = filter(
        lambda filename: filename.endswith(".py") and filename != "__init__.py",
        os.listdir(module_dir),
    )

    for command_module in command_modules:
        command_name = command_module[:-3]
        module = importlib.import_module(f"{module_dir}.{command_name}")

        try:
            handler_func = module.handler
            handler_filters = filters and module.handler_filters
            sync_sys_log(f'✅️ {module_dir}: "{command_name}" imported.')
        except AttributeError:
            sync_sys_log(
                f"⚠️ {module_dir}: The module {command_module} does not have 'handler'. Skip..."
            )
            continue

        args = []
        if named:
            app.add_handler(func(command_name, handler_func))
        elif pattern:
            app.add_handler(func(handler_func, pattern=f"^{command_name}:"))
        elif filters:
            app.add_handler(func(handler_filters, handler_func))
        else:
            app.add_handler(func(handler_func))
