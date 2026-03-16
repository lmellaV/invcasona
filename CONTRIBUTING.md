# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto!

## Cómo reportar bugs

Si encuentras un bug, por favor:

1. Verifica que el bug no haya sido reportado antes
2. Incluye mucha información:
   - Sistema operativo y versión
   - Versión de Python
   - Pasos exactos para reproducir
   - Comportamiento esperado vs actual
   - Capturas de pantalla si es relevante

## Cómo sugerir mejoras

Las sugerencias son bienvenidas. Por favor:

1. Usa un título claro y descriptivo
2. Proporciona una descripción clara de la sugerencia
3. Lista algunos ejemplos de cómo esta mejora sería útil
4. Menciona otras herramientas similares si aplica

## Pautas generales de desarrollo

### Ambiente de desarrollo

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Estructura de commits

- Usa mensajes claros y descriptivos
- Un cambio lógico por commit
- Referencia issues si aplica

**Ejemplo:**

```
Mejora: Agregar validación de tipos para factores de conversión (#15)

- Valida que Factor sea un número positivo
- Lanza excepción clara si es inválido
- Añade unit tests
```

### Testing

```bash
pytest tests/
```

### Código

- Sigue PEP 8
- Usa type hints donde sea posible
- Comenta el código complejo
- Mantén funciones pequeñas y enfocadas

## Proceso de pull request

1. Fork el proyecto
2. Crea un branch para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

### Checklist antes de enviar PR

- [ ] El código sigue las pautas de estilo
- [ ] He actualizado la documentación
- [ ] Mis cambios generan advertencias nuevas
- [ ] He añadido tests que prueban mi feature
- [ ] Los tests nuevos y existentes pasan

## Preguntas

Para preguntas generales, contacta al equipo de desarrollo.

---

**¡Gracias por contribuir!** 🎉
