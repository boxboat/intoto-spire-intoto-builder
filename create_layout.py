#!/bin/env python
from securesystemslib import interface
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock

def main():
  key_owner = interface.import_rsa_privatekey_from_file("./keys/owner")
  key_clone = interface.import_rsa_publickey_from_file("./keys/clone.pub")
  key_build = interface.import_rsa_publickey_from_file("./keys/build.pub")
  key_build_image = interface.import_rsa_publickey_from_file("./keys/build-image.pub")

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          key_clone["keyid"]: key_clone,
          key_build["keyid"]: key_build,
          key_build_image["keyid"]: key_build_image,
      },
      "steps": [{
          "name": "clone",
          "expected_materials": [["DISALLOW", "*"]],
          "expected_products": [["CREATE", "*"]],
          "pubkeys": [key_clone["keyid"]],
          "expected_command": [
              "git",
              "clone",
              "https://gitlab.com/boxboat/demos/intoto-spire/go-hello-world"
          ],
          "threshold": 1,
        },{
          "name": "build",
          "expected_materials": [
              ["MATCH", "*", "WITH", "PRODUCTS", "FROM", "clone"],
              ["DISALLOW", "*"]
          ],
          "expected_products": [["CREATE", "go-hello-world"], ["DISALLOW", "*"]],
          "pubkeys": [key_build["keyid"]],
          "expected_command": ["go", "build", "./..."],
          "threshold": 1,
        },{
          "name": "build-image",
          "expected_materials": [
              ["MATCH", "*", "WITH", "PRODUCTS", "FROM", "clone"],
              ["DISALLOW", "*"]
          ],
          "expected_products": [
              ["CREATE", "image-id"],
              ["CREATE", "go-hello-world.tar"],
              ["DISALLOW", "*"]],
          "pubkeys": [key_build_image["keyid"]],
          "threshold": 1,
        }
      ],
      "inspect": []
  })

  metadata = Metablock(signed=layout)

  # Sign and dump layout to "root.layout"
  metadata.sign(key_owner)
  metadata.dump("root.layout")

if __name__ == '__main__':
  main()
