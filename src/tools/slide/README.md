# Estructura Modular de Slide Tools

Este directorio contiene las herramientas de operaciones de slides organizadas de forma modular para mejorar la mantenibilidad y legibilidad del código.

## Estructura

```
slide/
├── __init__.py              # Exporta SlideTools
├── base.py                  # Clase principal que integra todas las operaciones
├── schemas.py               # Definiciones de esquemas de herramientas MCP
├── basic_operations.py      # Operaciones CRUD básicas
├── navigation_operations.py # Operaciones de navegación e información
├── layout_operations.py     # Operaciones de layouts
└── README.md               # Esta documentación
```

## Módulos

### 1. `base.py`
- **Propósito**: Clase principal `SlideTools` que integra todas las operaciones
- **Responsabilidades**: 
  - Inicializar el AppleScriptRunner
  - Crear instancias de las clases de operaciones especializadas
  - Delegar llamadas a los métodos apropiados
  - Mantener la interfaz pública compatible

### 2. `schemas.py`
- **Propósito**: Definiciones de esquemas de herramientas MCP
- **Responsabilidades**:
  - Definir los esquemas JSON de entrada para cada herramienta
  - Mantener toda la documentación de parámetros centralizada
  - Facilitar la modificación de esquemas sin tocar la lógica

### 3. `basic_operations.py`
- **Propósito**: Operaciones CRUD básicas de slides
- **Herramientas incluidas**:
  - `add_slide`: Agregar nuevos slides
  - `delete_slide`: Eliminar slides
  - `duplicate_slide`: Duplicar slides
  - `move_slide`: Mover slides de posición

### 4. `navigation_operations.py`
- **Propósito**: Operaciones de navegación e información
- **Herramientas incluidas**:
  - `get_slide_count`: Obtener número de slides
  - `select_slide`: Seleccionar un slide específico
  - `get_slide_info`: Obtener información detallada de un slide

### 5. `layout_operations.py`
- **Propósito**: Operaciones relacionadas con layouts
- **Herramientas incluidas**:
  - `set_slide_layout`: Cambiar el layout de un slide
  - `get_available_layouts`: Listar layouts disponibles

## Ventajas de la Modularización

### ✅ Mantenibilidad
- Archivos más pequeños y focalizados (50-100 líneas vs 426 líneas)
- Responsabilidades claramente separadas
- Fácil localización de código específico

### ✅ Escalabilidad
- Agregar nuevas operaciones es más simple
- Cada tipo de operación puede evolucionar independientemente
- Facilita la adición de nuevas categorías de herramientas

### ✅ Testeo
- Tests más específicos y focalizados
- Posibilidad de mockear módulos individuales
- Aislamiento de funcionalidades para debugging

### ✅ Reutilización
- Componentes pueden ser reutilizados en otros contextos
- Lógica de AppleScript separada por funcionalidad
- Esquemas reutilizables para validación

## Compatibilidad

La refactorización mantiene **100% de compatibilidad** con el código existente:
- La interfaz pública de `SlideTools` permanece idéntica
- Todos los métodos públicos funcionan exactamente igual
- Los imports existentes continúan funcionando sin cambios

## Uso

```python
from src.tools.slide import SlideTools

# Uso exactamente igual que antes
slide_tools = SlideTools()
tools = slide_tools.get_tools()
result = await slide_tools.add_slide(layout="Title Slide")
```

## Migración desde el archivo único

Si necesitas acceder a las operaciones específicas directamente:

```python
# Para operaciones básicas
from src.tools.slide.basic_operations import SlideBasicOperations

# Para operaciones de navegación
from src.tools.slide.navigation_operations import SlideNavigationOperations

# Para operaciones de layout
from src.tools.slide.layout_operations import SlideLayoutOperations
```

## Consideraciones de Desarrollo

- Cada módulo maneja sus propios errores específicos
- El AppleScriptRunner se comparte entre todos los módulos
- Las validaciones se realizan en cada módulo según corresponda
- Todos los métodos mantienen el mismo patrón de retorno `List[TextContent]`
