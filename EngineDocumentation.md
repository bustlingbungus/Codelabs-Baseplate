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

> aside negative
> There are some systems that involve objects referencing objects that they are neither a parent nor child of. The two main examples of this are texture rendering and collision checks, both of which will be described more in depth later. 

In order for `TextureRenderer` components to be rendered by a camera object, when a camera is updated, it will iterate through every `TextureRenderer` component and render it relative to itself. In order to find these texture renderrs, rather than traverse through the scene tree in search, there is a global array that stores a reference to all `TextureRenderer` components. This way, cameras can quickly render without having to first search. 

Likewise, in order to determine collision, `BoxCollider` components need to check all other box collider components. So, rather than have to traverse the scene tree in search, there is a global array for managing references to all `BoxCollider` components. 

There are also some systems that are not necessarily relevant to to the scene's tree structure. For instance, collecting user input, and calculating framerate are handled outside of the game's scenes, though they may be accessed by objects within the game. Here is a more comprehensive map of what a game in this engine might look like: 

![Comprehensive Model](img/concepts/BIG.PNG)

## Creating Custom Game Objects and Components

### Creating a Subclass

Any and all of the standard objects types in the API can be used as a template by just creating a subclass of said object. The main two baseplate game obects for this purpose will be `GameObject` itself, and `ObjectComponent`s.

> aside negative
> In order for a custom object to be useable, the constructor and deconstrucor functions <i>must</i> be defined. 

``` C++
/* MyObject.hpp */
#pragma once
#include "engine/BungusEngine.hpp"

class MyObject : public GameObject
{
    public:

        MyObject(Vector2 pos, Vector2 size, float speed);
        ~MyObject();

        virtual void Destroy();

        virtual void AssignComponents(shared_ptr<GameObject> self);
        virtual void Update();

    private:

        float speed;
};
```

``` C++
/* MyComponent.hpp */
#pragma once
#include "engine/BungusEngine.hpp"
using namespace std;

class MyComponent : public ObjectComponent
{
    public:

        MyComponent(shared_ptr<GameObject> parent);
        ~MyComponent();

        virtual void Destroy();

        virtual void Update();

    private:

        // EXAMPLE: stores a reference to parent's rigidbody component
        shared_ptr<Rigidbody> parent_rigid;
};
```

> aside positive
> Let's talk about the functions that are being redefined in the above examples:

<b>Constructor/Destructor:</b>

These are just part standard C++ subclass definitions. The main things to mention are, for the constructor, any arguments you like may be used, so long as you fill out the base class' constructor args. Importantly, in the destructor function, it is standard in this engine for the destructory to <i>only</i> call `Destroy()`, nothing more and nothing less.

``` C++
/* MyObject.cpp */

// constructor
MyObject::MyObject(Vector2 pos, Vector2 size, float speed)
: GameObject(pos, size), speed(speed)
{}

// destructor
MyObject::~MyObject() { Destroy(); }
```

``` C++
/* MyComponent.cpp */

// constructor
MyComponent::MyComponent(shared_ptr<GameObject> parent)
: ObjectComponent(parent)
{
    // EXAMPLE: stores a reference to parent's rigidbody component
    parent_rigid = parent->GetComponent<Rigidbody>();
}

// destructor
MyComponent::~MyComponent() { Destroy(); }
```

<b>Destroy</b>

This is the main function used for resource deallocation, and should be used as though it is the deconstructor. Importantly, within the Destroy function, you must call the base class' `Destroy()` function, because the base definitions for `Destroy` handle important resource management for game objects.

``` C++
/* MyObject.cpp */

// no additional cleanup required
void MyObject::Destroy() {
    GameObject::Destroy();  // make sure to call base's destroy
}
```

``` C++
/* MyComponent.cpp */

void MyComponent::Destroy() {
    ObjectComponent::Component();
    parent_rigid = nullptr; // additional cleanup required
}
```

<b>AssignComponents</b>

There are a few ways to add a component to a game object. You can just call `obj->AddComponent<Type>(...)`, though there also exist methods to add given components on instantiation. i.e., you can give an object specific components from the moment it's created. This is done in the `AssignComponents` function. The argument to this function will be the object itself, but as a shared pointer. This is done because object components rely on shared pointers, and aren't compatible with the `this` raw pointer accessible from within a class. 

Within `AssignComponents`, use `AddComponent` to add a given component to the object itself.

``` C++
/* MyObject.cpp */
#include "MyComponent.hpp"

// EXAMPLE: give self a rigidbody, texture renderer, and `MyComponent`
void MyObject::AssignComponents(shared_ptr<GameObject> self)
{
    // create a texture for texture renderer
    auto tex = make_shared<LTexture>(gWindow); // textures are made with reference to the global window
    tex->solidColour({255,255,255,255});
    // add texture renderer component
    AddComponent<TextureRenderer>(self, tex);

    // add rigidbody component. rigidbodies automatically add a box collider as well
    AddComponent<Rigidbody>(self, 1, 0.05);

    // add custom object component
    AddComponent<MyComponent>(self);
}
```

> aside positive
> `AssignComponents(self)` is called automatically on an object when it is instantiated, so you do not need to call this function manually.\

<b>Update</b>

This is the main behaviour function that will be called once per frame. If you want an object to have some special code that executes every frame, it should be put in `Update`.

``` C++
/* MyObject.cpp */

void MyObject::Update() {
    // example update
    position *= speed * gTime.deltaTime(); 
}
```

``` C++
/* MyComponent.cpp */

void MyComponent::Update() {
    // EXAMPLE: kill parent velocity
    parent->rigid->SetVelocity(Vector2_Zero);
}
```

### Adding Objects Into the Game

> aside negative
> there will also be some more complicated ways to add objects when defining custom scenes, which will be discussed later.

The `Instantiate` function will instantiate the desired game object type into the scene. The arguments of `Instantiate` vary, it takes the arguments used in the constructor of the object being created. For instance, in this example we Instantiate a `MyObject`, so the function will take a Vector2, a Vector2, then a float. Due to technical limitations, there are not dynamic tooltips to show the arguments of Instantiate, so it important to consult the class constructor of whatever object you are trying to create.

> aside negative
> WARNING: using arguments that are not suitable for the constructor of the object type will result in a crash!

Instantiate will create a new game object with the arguments provided, and add it into the current scene by adding the object as a child node of the current scene. The function also returns the shared pointer to the object created.

``` C++
/* in main.cpp (or anywhere really) */

// adds a MyObject into the game
// stores it pointer to obj
auto obj = Instantiate<MyObject>(
    Vector2_Zero, 
    Vector2(50, 75),
    400.0f
);
```

## Documentation: SDL

This section will outline the use and functionality of the SDL baseplate classes and their functions.

### <b>LWindow</b>

> aside negative
> Before discussing the LWindow class, it is important to note this engine makes use of one globally accessible LWindow pointer, `gWindow`. gWindow should be used for all SDL functions that involve a window, and you should not define any LWindow objects other than gWindow.

The LWindow stores an SDL_Window and SDL_Renderer. The window is the main window opened and used by the game, and the renderer is the global renderer used for most rendering functions in this API. The LWindow also performs all the neccesary initilisations for SDL in its constructor, which allows functionality of all SDL processes. This initialisation is why it's important to not create any addional LWindow objects.

The LWindow also contains a `gFont` member as a public member. This is a default font used when no font is specified for text rendering functions. This default font is white, 18 point Arial. 

### constructor

Initalises window variables and SDL.

<b>Arguments:</b>

* `width : int` - Window width (in pixels)
* `height : int` - Window height (in pixels)
* `name : std::string` - The Window's title

<b>Other Notes:</b>

* SDL is initalised with the flags `SDL_INIT_VIDEO`, `SDL_INIT_AUDIO`
* SDL_mixer is initialised with the flags `MIX_INIT_MP3`
* Linear texture filtering is enabled
* The renderer is created with index -1, and flags `SDL_RENDERER_ACCELERATED`
* Renderer draw colour is initialised to RGBA: 0,0,0,0
* SDL_image is initialised with flags `IMG_INIT_PNG`
* The default Arial font is loaded from "../../assets/DefaultFont.ttf", this file cannot be moved, deleted, renamed, or otherwise missing.

### deconstructor

Deallocates all resources by destroying renderer and window, freeing gFont, and quitting all SDL subsystems.

> aside negative
> WARNING: SDL will no longer be usable if you somehow create code <i>after</i> this deconstructor is called

### handleEvent

Performs updates and tracks changes in focus based on SDL window events. Changes window scale if the window is resized.

Complexity: O(1) time, O(1) memory

<b>Returns:</b> void

<b>Arguments:</b>

* `e : SDL_Event&` - Object containing event information.

<b>Other Notes:</b>

* This function is currently called in the event loop of the main window loop, this should not be changed. 

### setName

Changes the window's title.

<b>Returns:</b> void

<b>Arguments:</b>

* `newName : std::string` - The new window title.

### toggleFullscreen

