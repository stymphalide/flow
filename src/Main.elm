module Main exposing (..)

import Html exposing (program)
import Svg exposing (..)
import Svg.Attributes exposing(..)
import WebSocket

import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)

import List

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
type alias Position= 
    {x : Int, y : Int}

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
view : Model -> Html.Html Msg
view model =
    case model of
        Err err ->
            Html.text err
        Ok game ->
            svg [width "500", height "700"]
            <| List.concat [ (viewGrid {x = 0, y = 0} game.grid), viewColors]
viewGrid : Position ->  Grid Int -> List (Svg Msg)
viewGrid pos grid =
    List.concat <| List.map2 viewRow (positions "y" pos) grid
viewRow : Position -> List Int -> List (Svg Msg)
viewRow pos row =
    List.map2 viewCell (positions "x" pos) row
viewCell : Position -> Int -> Svg Msg
viewCell pos cell =
    rect 
    [ fill <| numberToColor cell
    , pos.x |> toString |> x
    , pos.y |> toString |> y
    , width "45"
    , height "45"
    , rx "8"
    , ry "8" 
    ] []
numberToColor color =
    case color of
        0 -> "rgb(50,109,173"
        1 -> "rgb(109, 252, 255)"
        2 -> "rgb(255, 252, 109)"
        3 -> "rgb(52, 219, 144)"
        4 -> "rgb(219, 52, 52)"
        5 -> "rgb(224,124,17)"
        _ -> "rgb(0,0,0)"
viewColors =
    viewRow {x = 0, y = 650} [0,1,2,3,4,5]
positions : String ->  Position -> List Position
positions axis pos =
    case axis of
        "x" ->
            [pos, {pos | x = pos.x + 50}, {pos | x = pos.x + 100}, {pos | x = pos.x + 150}, {pos | x = pos.x + 200}, {pos | x = pos.x + 250}, {pos | x = pos.x + 300}, {pos | x = pos.x + 350}, {pos | x = pos.x + 400}, {pos | x = pos.x + 450}]
        _ ->
            [pos, {pos | y = pos.y + 50}, {pos | y = pos.y + 100}, {pos | y = pos.y + 150}, {pos | y = pos.y + 200}, {pos | y = pos.y + 250}, {pos | y = pos.y + 300}, {pos | y = pos.y + 350}, {pos | y = pos.y + 400}, {pos | y = pos.y + 450}]
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