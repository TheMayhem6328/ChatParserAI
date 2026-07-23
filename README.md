# Chat Parser AI

## Note

VERY messy code right now. To be refactored and documented once parsing works properly

## Env

Tested on Py 3.14.6 on Win11 and WSL Ubuntu

## Procedural Stuff

Python types generated from schema using:

```sh
datamodel-codegen --input chat_data.schema.json --output rough/stuff.py --preset practical-py314-20260619 --output-model-type pydantic_v2.BaseModel
```

## Files

- `telegram_html.py` - reads Telegram official exports

## To-Do
- [ ] Telegram
  - [ ] Reply context
  - [ ] Media
    - [X] Image/Video
    - [X] GIF
    - [ ] Calls
- [ ] Schema
  - [ ] Message
    - [ ] Calls
- [ ] Discord
- [ ] Overall
  - [ ] Better file/directory layout and nomenclature
  - [ ] Proper documentation of schema
  - [ ] Refactoring of `chat_data_types.py`
  - [ ] Implementation of SQLite storage of texts
- [ ] AI thingamajik

## Credits

Major props to [file-windows](https://github.com/nscaife/file-windows/)
