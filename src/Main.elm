module Main exposing (..)

import Html exposing (program)
import Html.Attributes  as A
import Svg exposing (..)
import Svg.Attributes exposing(..)
import Svg.Events exposing (onClick)
import WebSocket

import Json.Encode as Encode
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
    | Play Int

type alias Grid a =
    List (List a)
type alias Position= 
    {x : Int, y : Int}

serverUrl =
    "ws://localhost:5000"


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
        Play color ->
            case model of
                Ok game ->
                    (model, WebSocket.send serverUrl (encodePlay game color ))
                Err err ->
                    (model, Cmd.none)

-- INIT
init : (Model, Cmd Msg)
init =
    (Err "start", WebSocket.send serverUrl (Encode.encode 0 (Encode.string "start")))

-- VIEW
view : Model -> Html.Html Msg
view model =
    case model of
        Err err ->
            Html.text err
        Ok game ->
            if game.ended then
                Html.div [A.class "center"] 
                [ Html.h1 [] [text "Flow"]
                , Html.h2 [] [text <| toString game.score]
                , Html.h2 [] [text "You Won!"]
                , svg [width "500", height "700"]
                <| List.concat [ (viewGrid {x = 0, y = 0} game.grid)]
                ]
            else
                Html.div [A.class "center"] 
                [ Html.h1 [] [text "Flow"]
                , Html.h2 [] [text <| toString game.score]
                , svg [width "500", height "700"]
                <| List.concat [ (viewGrid {x = 0, y = 0} game.grid), viewColors]
                ]
viewGrid : Position ->  Grid Int -> List (Svg Msg)
viewGrid pos grid =
    List.concat <| List.map2 (viewRow False) (positions "y" pos) grid
viewRow : Bool -> Position -> List Int -> List (Svg Msg)
viewRow isClick pos row =
    List.map2 (viewCell isClick) (positions "x" pos) row
viewCell : Bool -> Position -> Int -> Svg Msg
viewCell isClick pos cell =
    if isClick then
        rect 
        [ fill <| numberToColor cell
        , pos.x |> toString |> x
        , pos.y |> toString |> y
        , width "45"
        , height "45"
        , rx "8"
        , ry "8"
        , onClick <| Play cell
        ] []
    else
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
    viewRow True {x = 0, y = 650} [0,1,2,3,4,5]
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
    WebSocket.listen serverUrl GameState
-- Decoder
gameDecoder : Decode.Decoder Game
gameDecoder =
    decode Game
    |> required "grid" (Decode.list (Decode.list Decode.int))
    |> required "control_grid"  (Decode.list (Decode.list Decode.bool))
    |> required "score" Decode.int
    |> required "ended" Decode.bool
-- Encoder
encodePlay : Game -> Int -> String
encodePlay game color =
    Encode.object
        [ ("color", Encode.int color)
        , ("state", encodeGame game)
        ]
    |> (Encode.encode 0)
encodeGame : Game -> Encode.Value
encodeGame game =
    Encode.object
        [ ("grid", encodeIntGrid game.grid)
        , ("control_grid", encodeBoolGrid game.control_grid)
        , ("ended", Encode.bool game.ended)
        , ("score", Encode.int game.score)
        ]
encodeIntGrid : List (List Int) -> Encode.Value
encodeIntGrid grid =
    List.map encodeIntRow grid |> Encode.list
encodeIntRow : List Int -> Encode.Value
encodeIntRow list =
            List.map Encode.int list |> Encode.list
encodeBoolGrid : List (List Bool) -> Encode.Value
encodeBoolGrid grid =
    List.map encodeBoolRow grid |> Encode.list
encodeBoolRow : List Bool -> Encode.Value
encodeBoolRow list =
            List.map Encode.bool list |> Encode.list
-- MAIN
main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }