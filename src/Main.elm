module Main exposing (..)

import Html exposing (program, text)



type Model =
    NoState


type Msg =
    NoOp


-- UPDATE
update msg model =
    (model, Cmd.none)

-- INIT
init : (Model, Cmd Msg)
init =
    (NoState, Cmd.none)

-- VIEW
view model =
    text "Nothing to be seen yet."

-- SUBSCRIPTIONS
subscriptions model =
    Sub.none


-- MAIN
main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }