author: Caden Spokas
summary:
id: EngineDocumentation
tags:
categories:
environments: Web
status: Published
feedback link: https://github.com/bustlingbungus/Codelabs-Baseplate/tree/Engine_Build_Instructions

# Bungus Engine Documentation

## Overview

### Table of Contents

1. Overview (this page)

## Engine Visualisation

### The Game as a Tree

Each object in this engine can be viewed as the root of a tree structure. Every game object can have an arbitrary number of child objects (including none). Game objects contain an array of pointers to other game objects, their `components`. These components can do a number of things, they might reder a texture, perform collisoin checks, move their parent object around, etc. 

![Example of Game Object's relations](img/concepts/gameObjectStructure.PNG)

Importantly, these object components are also just game objects themselves. They're just specialised objects that contain a reference to their parent, which allows them to track and modify their parent in a specific way. 

It's not just specialised components that have to be shild objects, though. For organisational purposes, as well as code optimisation, regular game objects can be stored as children of another game object.

![Object container diagram](img/concepts/wallContainer.PNG)

This begs the question, how do we store and manage the base container game objects with no parents? To do this, we give all these parentless objects one parent game object: the scene itself. A scene in this engine is really just a game object, intended to be the root of the game object tree. Hence, the entire game can be thought of as a big tree structure, where each node is a game object, and a node's children are its components. 

Each game object and component needs to be updated every frame. To do this, starting at the root scene, The object is updated, then all of it's children are updated, recursively. In other words, game objects are updated in `preorder` traversal.

![Example Scene Structure](img/concepts/exampleSceneStructure.PNG)

Natually, you might wonder if anything could connect multiple scene nodes. Since these scens serve as root nodes, they are not connected like other game objects, though the game will store a hashmap of these scenes, in order to have an arbitrary number of trees, or scenes, in the game. Switching between scenes, therefore, is simply a matter of switching the root node that gets updated every frame.

### Global Management

There are some systems that involve objects referencing objects that they are neither a parent nor child of. The two main examples of this are texture rendering and collision checks, oth of which wil be described more in depth. 

In order for `TextureRenderer` components to be rendered by a camera object, when a camera is updated, it will iterate through every `TextureRenderer` component and render it relative to itself. In order to find these texture renderrs, rather than traverse through the scene tree in search, there is a global array that stores a reference to all `TextureRenderer` components. This way, cameras can quickly render without having to first search. 

Likewise, in order to determine collision, `BoxCollider` components need to check all other box collider components. So, rather than have to traverse the scene tree in search, there is a global array for managing references to all `BoxCollider` components. 

There are also some systems that are not necessarily relevant to to the scene's tree structure. For instance, collecting user input, and calculating framerate are handled outside of the game's scenes, though they may be accessed by objects within the game. Here is a more comprehensive map of what a game in this engine might look like: 

![Comprehensive Model](img/concepts/BIG.PNG)

## Creating Custon Game Objects and Components

### Creating a Subclass

