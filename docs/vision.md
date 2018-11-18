# Vision

This document is for describing the vision. We may eventually end up separating this with a higher level architectural diagram and a separate doc for implementation details.

## Why do we need containerisation

- On komodoplatform, we run a whole range of chains which get compiled, configured and deployed differently. Each of these may have different dependencies and it gets harder to test things in isoltation when we deploy all of these on a single server. We  would like to handle this problem through containerisation where self container docker images can be used to launch containers which work exactly the same irrespective of underlying operating system (and it's version).
- Compilation takes a while and occasionally we see 3rd party packages being missed. We would like to keep dockerhub images which have compiled version that can just be used without any fuss.
- Local testing on your laptops gets easier because you can just work with a container, make changes and then get it deployed onto your production environment.
