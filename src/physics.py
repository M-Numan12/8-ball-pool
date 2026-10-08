"""2D pool geometry for a screenshot-based, offline shot planner."""
from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True)
class Point:
    x: float
    y: float

def unit(a: Point, b: Point) -> Point:
    d = hypot(b.x-a.x,b.y-a.y)
    if d == 0: raise ValueError("Coincident points")
    return Point((b.x-a.x)/d,(b.y-a.y)/d)

def ghost_ball(target: Point, pocket: Point, radius: float) -> Point:
    if radius <= 0: raise ValueError("radius must be positive")
    u = unit(target,pocket)
    return Point(target.x - 2*radius*u.x, target.y - 2*radius*u.y)

def segment_distance(p: Point, a: Point, b: Point) -> float:
    dx,dy=b.x-a.x,b.y-a.y
    denom=dx*dx+dy*dy
    t=max(0,min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/denom)) if denom else 0
    return hypot(p.x-a.x-t*dx,p.y-a.y-t*dy)

def clear_path(a: Point, b: Point, obstacles: list[Point], radius: float) -> bool:
    return all(segment_distance(p,a,b)>2*radius for p in obstacles)

def suggest(cue: Point, targets: list[Point], pockets: list[Point], radius: float):
    shots=[]
    for i,target in enumerate(targets):
        for j,pocket in enumerate(pockets):
            try: ghost=ghost_ball(target,pocket,radius)
            except ValueError: continue
            others=[p for k,p in enumerate(targets) if k!=i]
            if clear_path(cue,ghost,others,radius) and clear_path(target,pocket,others+[cue],radius):
                score=hypot(cue.x-ghost.x,cue.y-ghost.y)+hypot(target.x-pocket.x,target.y-pocket.y)
                shots.append((score,i,j,ghost))
    return sorted(shots,key=lambda s:s[0])
