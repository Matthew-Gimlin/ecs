"""A simple ECS implementation.

An entity cannot contain multiple components of the same type. Likewise, a world
cannot contain multiple systems of the same type.
"""
from __future__ import annotations
from typing import Dict, Type, List, Optional
from collections import defaultdict

class Component:
    """A base class for components.
    """
    pass

class Entity:
    """A container for components.
    """
    def __init__(self) -> None:
        """Constructor.
        """
        self.components: Dict[Type[Component], Component] = {}

    def _has_component(self, component_type: Type[Component]) -> bool:
        """Checks if the entity contains a component.
        """
        return component_type in self.components

    def _get_component(
            self,
            component_type: Type[Component]
        ) -> Optional[Component]:
        """Gets an instance of a component for the entity.
        """
        return self.components.get(component_type, None)

    def _push_component(self, component: Component) -> None:
        """Adds a component to the entity.
        """
        self.components[type(component)] = component

    def _pop_component(self, component_type: Type[Component]) -> None:
        """Removes a component from the entity.
        """
        self.components.pop(component_type, None)

class System:
    """A base class for systems.
    """
    def update(self, world: World) -> None:
        """A virtual function to update the system.
        """
        pass

class World:
    """A container for entities, components, and systems.
    """
    def __init__(self) -> None:
        """Constructor.
        """
        self.entities: List[Entity] = []
        self.components: Dict[Type[Component], List[Entity]] = defaultdict(list)
        self.systems: List[System] = []

    def has_entity(self, entity: Entity) -> bool:
        """Checks if the world contains an entity.
        """
        return entity in self.entities

    def push_entity(self) -> Entity:
        """Creates an entity in the world.
        """
        entity = Entity()
        self.entities.append(entity)
        return entity

    def pop_entity(self, entity: Entity) -> None:
        """Remove an entity from the world.
        """
        self.entities.remove(entity)
        for component_type, entities in self.components.items():
            if entity in entities:
                entities.remove(entity)

    def has_component(
            self,
            entity: Entity,
            component_type: Type[Component]
        ) -> bool:
        """Checks if an entity contains a component.
        """
        return entity in self.components[component_type]

    def get_components(
            self,
            component_type: Type[Component]
        ) -> List[Component]:
        """Gets an instance of a component for all entities.
        """
        return [
            entity._get_component(component_type)
            for entity in self.components[component_type]
        ]

    def get_entities_by_component(
            self,
            component_type: Type[Component]
        ) -> List[Entity]:
        """Gets all entities that contain a component.
        """
        return self.components[component_type]

    def get_component_by_entity(
            self,
            entity: Entity,
            component_type: Type[Component]
        ) -> Optional[Component]:
        """Gets an instance of component for an entity.
        """
        return entity._get_component(component_type)

    def push_component(self, entity: Entity, component: Component) -> None:
        """Adds a component to an entity.
        """
        entity._push_component(component)
        self.components[type(component)].append(component)

    def pop_component(
            self,
            entity: Entity,
            component_type: Type[Component]
        ) -> None:
        """Removes a component from an entity.
        """
        entity._pop_component(component_type)
        if entity in self.components[component_type]:
            self.components[component_type].remove(entity)

    def has_system(self, system_type: Type[System]) -> bool:
        """Checks if the world contains a system.
        """
        return any([type(system) == system_type for system in self.systems])

    def get_system(self, system_type: Type[System]) -> Optional[System]:
        """Gets a system from the world.
        """
        return next(
            [system for system in self.systems if type(system) == system_type],
            None
        )

    def push_system(self, system: System) -> None:
        """Adds a system to the world.
        """
        self.systems.append(system)

    def pop_system(self, system_type: Type[System]) -> None:
        """Removes a system from the world.
        """
        system = self.get_system(system_type)
        if system:
            self.systems.remove(system)
