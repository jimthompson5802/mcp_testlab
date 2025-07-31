from fastmcp import FastMCP

mcp = FastMCP("MathTools")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: The first integer to add.
        b: The second integer to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a: The first integer to multiply.
        b: The second integer to multiply.

    Returns:
        int: The product of a and b.
    """
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")
