author: Caden Spokas
summary:
id: SDLBoilerplateDocumentation
tags:
categories:
environments: Web
status: Published
feedback link: https://github.com/bustlingbungus/Codelabs-Baseplate/tree/Engine_Build_Instructions

# SDL Boilerplate Documentation

## Table of Contents

This is documentation for the functions and methods found in Bustling Bungus' SDL boilerplate.

### Table of contents

1. Table of Contents (this page)
2. LWindow

## <b>LWindow</b>

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
* When changing window size, (including toggling fullscreen), the rendering scale will be changed accorindgly, so the sizes of rendered objects will not change relative to window size.

### setName

Changes the window's title.

<b>Returns:</b> void

<b>Arguments:</b>

* `newName : std::string` - The new window title.

### toggleFullscreen

Makes the window fullscreen if it isn't already. If the window is fullscreen, sets it to windowed mode. When returning to windowed mode, the window dimensions will be the same as they were before switching into fullscreen. 

<b>Returns: `bool`</b>, `true` when the window was made fullscreen, and `false` if it was set back to windowed mode.

<b>Other Notes:</b>

* When going into fullscreen, the `SDL_WINDOW_FULLSCREEN_DESKTOP` flag is used. 
* When changing window size, (including toggling fullscreen), the rendering scale will be changed accorindgly, so the sizes of rendered objects will not change relative to window size.

### hasMouseFocus

Whether or not the the window is "entered", i.e., has mouse focus.

<b>Returns:</b> bool

<b>Other Notes:</b>

* Set to `true` on `SDL_WINDOWEVENT_ENTER`.
* Set to `false` on `SDL_WINDOW_EVENT_LEAVE`.

### hasKeyboardFocus

Whether or not the window has keyboard focus.

<b>Returns:</b> bool

<b>Other Notes:</b>

* Set to `true` on `SDL_WINDOWEVENT_FOCUS_GAINED`.
* Set to `false` on `SDL_WINDOWEVENT_FOCUS_LOST`.

### isMinimized

Whether the window has been minimised.

<b>Returns:</b> bool

<b>Other Notes:</b>

* Set to `true` on `SDL_WINDOWEVENT_MINIMIZED`.
* Set to `false` on `SDL_WINDOWEVENT_MAXIMIZED` or `SDL_WINDOWEVENT_RESTORED`.

### getWidth

Returns the width of the window, in pixels.

<b>Returns:</b> int

### getHeight

Returns the height of the window, in pixels.

<b>Returns:</b> int

### getScaleX

Returns the rendering scale along the x axis.

<b>Returns:</b> float

<b>Other Notes:</b>

* Render scale is how much textures get stretched horizontally when rendered. 1.0 = no stretching.
* The render scale is updated automatically when the window dimensions are changed. 

### getScaleY

Returns the rendering scale along the x axis.

<b>Returns:</b> float

<b>Other Notes:</b>

* Render scale is how much textures get stretched vertically when rendered. 1.0 = no stretching.
* The render scale is updated automatically when the window dimensions are changed. 

## LTexture

This is a class used for storing a texture which may be rendered onto the window (or any other texture). When the texture is rendered with `render`, it will by default render directly onto the window. 

### constructor

Initialised variables to `NULL`. Set's the texture's window.

<b>Arguments:</b>

* `gHolder : std::shared_ptr<LWindow>` - A shared pointer to the window the texture should render to.

<b>Other Notes:</b>

* The texture is initialised to `NULL` in the constructor, so to be usable, one of the texture creation functions should be called. 

### deconstructor

Frees the texture by calling `free()`.

### free

Destroys the stored texture object and resets variables.

<b>Returns:</b> void

<b>other Notes:</b>

* Once this function is called, the texture will no longer be usable for rendering until it loads a new texture. 

### render (version: 1)

Renders a texture at a desired (x, y) pixel coordinate on the window. If no `dest` rect is provided, the dimensions of the texture will be used for the size of the rendering region.

<b>Returns:</b> void

<b>Arguments:</b>

* `x : int` - The x pixel coordinate on the window.
* `y : int` - The y pixel coordinate on the window.
* `dest : SDL_Rect*` - The rendering rect, used to set rendering region dimensions. Leave as `NULL` to use the dimensions of the texture itself.
* `clip : SDL_Rect*` - The source region from the texture itself. Defines a specific (x,y,w,h) region from the texture to render into the dest rect. Leave as `NULL` to use the entire texture as the source.
* `angle : 0.0` - The angle in degrees the texture will be rendered at, rotates the image in a clockwise direction.
* `center : SDL_Point*` - The center of rotation when using `angle` to rotate the texture. Leave as `NULL` to rotate about the texture's centre.
* `flip : SDL_RendererFlip` - The axis about which the rendered image will be flipped. By default is set to `SDL_FLIP_NONE` for no flipping.

<b>Other Notes:</b>

* Renders using it's window's `gRenderer` member. i.e., will render to whatever render target the window is set to, which will be the window itself assuming it is left as `NULL`.
* If the dimensions of the `dest` rect are different to the texture's source dimensions, the texture will be stretched or squashed to fit the desired dimensions.

### render (version: 2)

Renders a texture into the provided dest rect on the window. 

<b>Returns:</b> void

<b>Arguments:</b>

* `dest : SDL_Rect*` - The rendering rect, used to define the x and y pixel coordinates the image is rendered at, as well as the x and y dimensions (in pixels) of the rendered image.
* `clip : SDL_Rect*` - The source region from the texture itself. Defines a specific (x,y,w,h) region from the texture to render into the dest rect. Leave as `NULL` to use the entire texture as the source.
* `angle : 0.0` - The angle in degrees the texture will be rendered at, rotates the image in a clockwise direction.
* `center : SDL_Point*` - The center of rotation when using `angle` to rotate the texture. Leave as `NULL` to rotate about the texture's centre.
* `flip : SDL_RendererFlip` - The axis about which the rendered image will be flipped. By default is set to `SDL_FLIP_NONE` for no flipping.

<b>Other Notes:</b>

* Renders using it's window's `gRenderer` member. i.e., will render to whatever render target the window is set to, which will be the window itself assuming it is left as `NULL`.
* If the dimensions of the `dest` rect are different to the texture's source dimensions, the texture will be stretched or squashed to fit the desired dimensions.

### renderAsBackground

Renders the texture, stretched (or squashed) to fit the window dimensions, centred at the window's centre.

<b>Returns:</b> void

<b>Arguments:</b>

* `clip : SDL_Rect*` - The source region from the texture itself. Defines a specific (x,y,w,h) region from the texture to render into the dest rect. Leave as `NULL` to use the entire texture as the source.
* `angle : 0.0` - The angle in degrees the texture will be rendered at, rotates the image in a clockwise direction.
* `center : SDL_Point*` - The center of rotation when using `angle` to rotate the texture. Leave as `NULL` to rotate about the texture's centre.
* `flip : SDL_RendererFlip` - The axis about which the rendered image will be flipped. By default is set to `SDL_FLIP_NONE` for no flipping.

<b>Other Notes:</b>

* Renders using it's window's `gRenderer` member. i.e., will render to whatever render target the window is set to, which will be the window itself assuming it is left as `NULL`.

### render_toTexture (version: 1)

Render's the texture onto another texture object. Does this by setting the window's render target to the other texture's texture, rendering normally, then resetting the window's render target. 

> aside negative
> WARNING: This function will cause a crash if the `target` texture was not created with `SDL_RENDERACCESS_TARGET`. Currently, only textures created with `solidColour` create textures with this access type. One easy workaround is to just create a blank solid colour texture of the desire dimensions (alpha=0), then render any images and whatnot you like onto said texture. 

<b>Returns:</b> void

<b>Arguments:</b>

* `target : LTexture*` - Raw pointer to the texture being rendered to.
* `x : int` - The x pixel coordinate on the other texture.
* `y : int` - The y pixel coordinate on the other texture.
* `dest : SDL_Rect*` - The rendering rect, used to set rendering region dimensions. Leave as `NULL` to use the dimensions of the texture itself.
* `clip : SDL_Rect*` - The source region from the texture itself. Defines a specific (x,y,w,h) region from the texture to render into the dest rect. Leave as `NULL` to use the entire texture as the source.
* `angle : 0.0` - The angle in degrees the texture will be rendered at, rotates the image in a clockwise direction.
* `center : SDL_Point*` - The center of rotation when using `angle` to rotate the texture. Leave as `NULL` to rotate about the texture's centre.
* `flip : SDL_RendererFlip` - The axis about which the rendered image will be flipped. By default is set to `SDL_FLIP_NONE` for no flipping.

### render_toTexture (version: 2)

Render's the texture onto another texture object. Does this by setting the window's render target to the other texture's texture, rendering normally, then resetting the window's render target. 

> aside negative
> WARNING: This function will cause a crash if the `target` texture was not created with `SDL_RENDERACCESS_TARGET`. Currently, only textures created with `solidColour` create textures with this access type. One easy workaround is to just create a blank solid colour texture of the desire dimensions (alpha=0), then render any images and whatnot you like onto said texture. 

<b>Returns:</b> void

<b>Arguments:</b>

* `target : LTexture*` - Raw pointer to the texture being rendered to.
* `dest : SDL_Rect*` - The rendering rect, used to define the x and y pixel coordinates the image is rendered at, as well as the x and y dimensions (in pixels) of the rendered image.
* `angle : 0.0` - The angle in degrees the texture will be rendered at, rotates the image in a clockwise direction.
* `center : SDL_Point*` - The center of rotation when using `angle` to rotate the texture. Leave as `NULL` to rotate about the texture's centre.
* `flip : SDL_RendererFlip` - The axis about which the rendered image will be flipped. By default is set to `SDL_FLIP_NONE` for no flipping.

### getWidth

Returns the image width in pixels.

<b>Returns:</b> int

<b>Other Notes:</b> Image width is zero if the image isn't yet loaded, or otherwise invalid.

### getHeight

Returns the image height in pixels.

<b>Returns:</b> int

<b>Other Notes:</b> Image height is zero if the image isn't yet loaded, or otherwise invalid.

### loadFromFile

Loads an image from the specified file path as a texture. Returns true/false for the success of the operation.

<b>Returns:</b> bool

<b>Arguments:</b>

* `path : std::string` - The directory (relative to the actual .exe excutable) and filename of the file to load. Must be an image file.

<b>Other Notes:</b>

* The created texture will have access type `SDL_TEXTUREACCESS_STATIC`.

### loadFromRenderedText

Creates a texture from a string. Allows for customisable text colour and font. Returns true/false for the success of the operation.

<b>Returns:</b> bool

<b>Arguments:</b>

* `textureText : std::string` - The text to be convertex into a texture. Must be a non empty string (i.e., anything but `""`).
* `textColor : SDL_Color` - The colour of the text. White by default.
* `font : TTF_Font*` - raw pointer to a ttf font, which includes font size and the font itself. If left as `nullptr`, the texture's window's `gFont` (18 point Arial) will be used. 

<b>Other Notes:</b>

* This function takes a raw pointer to a `TTF_Font`, in spite of the `LFont` class. To get a `TTF_Font` pointer from an `LFont`, use `myFont->get()`.
* This function is only available if `SDL_TTF_MAJOR_VERSION` is defined. i.e., if you have SDL_ttf installed. 
* The created texture will have access type `SDL_TEXTUREACCESS_STATIC`.

### solidColour

Makes the texture a single, solid colour for its whole dimensions. Returns true/false for the success of the operation

<b>Returns:</b> bool

<b>Arguments:</b>

* `colour : SDL_Colour` - The RGBA colour to create. 
* `width : int` - The texture width in pixels. 1 by default.
* `height : int` - The texture height in pixels. 1 by default.

<b>Other Notes:</b>

* A completely transparent texture can be created by passing a colour argument with alpha = 0. This could be useful for creating a transparent background to render other textures onto.
* Texture is created with format `SDL_PIXELFORMAT_RGBA8888` and access hint `SDL_TEXTUREACCESS_TARGET`.

### setColor

Sets texture colour modulation. i.e., masks the texture with the defined rgb colour.

<b>Returns:</b> void

<b>Arguments:</b>

* `red : Uint8` - Red colour modulation.
* `green : Uint8` - Green colour modulation.
* `blue : Uint8` - Blue colour modulation.

### setAlpha

Sets texture alpha modulation. i.e., reduces pixel alpha to the given value.

<b>Returns:</b> void

<b>Arguments:</b>

* `alpha : Uint8` - Alpha modulation

### setBlendMode

Sets the texture blend mode.

<b>Returns:</b> void

<b>Arguments:</b>

* `blending : SDL_BlendMode` - The desired blend mode.

## LAudio

Class for loading and playing audio. Will play audio into a number of different channels. Channel zero can only be accessed manually, not by the automatic channel picking system. This is intended to have a "reserved" channel for music, that can't be interrupted by automatic channel picking.

There are 8 total channels to choose from. Without the reseved channel 0, this makes 7 free audio channels. If you play an audio while all 7 of these channels are playing audio, one of these channels will be interrupted to play the new audio. 

