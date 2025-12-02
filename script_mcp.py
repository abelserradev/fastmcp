import asyncio
from app.mcp.tools import (
    consultar_persona_handler,
    consultar_cotizacion_handler,
    consultar_poliza_handler,
)

async def test_tools():
    print("\n" + "="*50)
    
    print("\n1. Probando consultar_persona...")
    try:
        result = await consultar_persona_handler({
            "num_documento": "V-26745518"
        })
        print("Resultado:", result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n2. Probando consultar_cotizacion...")
    try:
        result = await consultar_cotizacion_handler({
            "nu_cotizacion": 12345,
            "cd_entidad": 1
        })
        print("Resultado:", result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n3. Probando consultar_poliza...")
    try:
        result = await consultar_poliza_handler({
            "cd_entidad": 1,
            "cd_area": 1,
            "poliza": 12345,
            "certificado": 1
        })
        print("Resultado:", result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tools())