from fastapi import APIRouter, HTTPException
from models.tarea import TareaEntrada, TareaActualizacion, TareaSalida
from datetime import datetime
from typing import Optional

router = APIRouter()

tareas = []
contador_id = 1

@router.get("/tareas")
def listar_tareas(completada: Optional[bool] = None, prioridad: Optional[str] = None):
    resultado = tareas
    if completada is not None:
        resultado = [t for t in resultado if t["completada"] == completada]
    if prioridad is not None:
        resultado = [t for t in resultado if t["prioridad"] == prioridad]
    return resultado

@router.get("/tareas/estadisticas")
def estadisticas():
    total = len(tareas)
    completadas = len([t for t in tareas if t["completada"]])
    pendientes = total - completadas
    por_prioridad = {"baja": 0, "media": 0, "alta": 0}
    for t in tareas:
        if not t["completada"]:
            por_prioridad[t["prioridad"]] += 1
    return {"total": total, "completadas": completadas, "pendientes": pendientes, "pendientes_por_prioridad": por_prioridad}

@router.get("/tareas/{id}")
def obtener_tarea(id: int):
    for t in tareas:
        if t["id"] == id:
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@router.post("/tareas", status_code=201)
def crear_tarea(tarea: TareaEntrada):
    global contador_id
    nueva = {
        "id": contador_id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad": tarea.prioridad,
        "completada": False,
        "creada_en": datetime.now(),
        "completada_en": None,
        "fecha_limite": tarea.fecha_limite
    }
    tareas.append(nueva)
    contador_id += 1
    return nueva

@router.patch("/tareas/{id}")
def actualizar_tarea(id: int, cambios: TareaActualizacion):
    for t in tareas:
        if t["id"] == id:
            if cambios.titulo is not None:
                t["titulo"] = cambios.titulo
            if cambios.descripcion is not None:
                t["descripcion"] = cambios.descripcion
            if cambios.prioridad is not None:
                t["prioridad"] = cambios.prioridad
            if cambios.completada is not None:
                t["completada"] = cambios.completada
            if cambios.fecha_limite is not None:
                t["fecha_limite"] = cambios.fecha_limite
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@router.delete("/tareas/{id}", status_code=204)
def eliminar_tarea(id: int):
    for i, t in enumerate(tareas):
        if t["id"] == id:
            tareas.pop(i)
            return
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@router.post("/tareas/{id}/completar")
def completar_tarea(id: int):
    for t in tareas:
        if t["id"] == id:
            t["completada"] = True
            t["completada_en"] = datetime.now()
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")