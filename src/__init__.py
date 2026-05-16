# Lazy re-export mcp from server module
# Using __getattr__ ensures tools always get the current (possibly patched) instance
def __getattr__(name):
    if name == "mcp":
        from src.server import mcp
        return mcp
    raise AttributeError(name)
