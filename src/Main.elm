module Main exposing (..)

import Html exposing (program, text)
import WebSocket

import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)

type alias Model =
    Result String Game


type alias Game =
    { grid : Grid Int
    , control_grid : Grid Bool
    , score : Int
    , ended : Bool
    }

type Msg 
    = NoOp
    | GameState String

type alias Grid a =
    List (List a)

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        NoOp ->
            (model, Cmd.none)
        GameState gameString ->
            let
                resGame =
                    Decode.decodeString gameDecoder gameString
            in
                (resGame, Cmd.none)

-- INIT
init : (Model, Cmd Msg)
init =
    (Ok initialGame, Cmd.none)
initialGame =
    {grid = [[0, 0], [0,0]], control_grid = [[False, False], [False, False]], score = 0, ended = False}

-- VIEW
view model =
    text <| toString model

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    WebSocket.listen "ws://localhost:5000/" GameState
-- Decoder
gameDecoder : Decode.Decoder Game
gameDecoder =
    decode Game
    |> required "grid" (Decode.list (Decode.list Decode.int))
    |> required "control_grid"  (Decode.list (Decode.list Decode.bool))
    |> required "score" Decode.int
    |> required "ended" Decode.bool


-- MAIN
main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }