
DEBUG_LOGGING = true -- Set to true to enable logging

-- Helper function to log to console and also send debug messages
local function log(message)
    if DEBUG_LOGGING then   
        sendDebugMessage(message, "Extractor")
        print("[Extractor] " .. message)
    end
end

log("Loading Extractor module...")

-- Load the condig with SMOD
local config = SMODS.current_mod.config
log("Config loaded: " .. inspect(config))

-- Load required modules
local https = require "SMODS.https"
local json = require "json"
log("Loaded required modules")

-- Hopefully prevents some errors trying to access userdata, which cannot be serialized to JSON
local function convert_type(some_data)
    -- This function ensures that the data we're trying to send is in a format that can be serialized to JSON.
    local allowed_types = {
        ["string"] = true,
        ["number"] = true,
        ["boolean"] = true,
        ["table"] = true,
        ["nil"] = true
    }

    local data_type = type(some_data)
    if allowed_types[data_type] then
        return some_data
    else
        log("Unsupported data type: " .. data_type .. ". Converting to string.")
        return tostring(some_data)
    end
end

-- Leaving this function here in case I need it later
-- This function explores a table and returns a JSON string representation of it
-- It will not explore any key called "parent" or "children" to avoid useless recursion
local function table_explore(table, current_depth)
    if not current_depth then
        current_depth = 0  -- Initialize depth if not provided
    end

    if current_depth > 5 then
        log("Maximum recursion depth reached. Stopping exploration.")
        return {}  -- Return an empty JSON object if depth exceeds limit
    end

    -- This function fully explores a table, and returns it as a json string
    -- If the table encounters another table, then it will recursively explore that table, adding the result to the json string
    -- It will not explore any key called "parent" to avoid infinite recursion

    local result = {}
    for key, value in pairs(table) do
        if key ~= "parent" and key ~= "children" then  -- Avoid infinite recursion
            if type(value) == "table" then
                result[key] = table_explore(value, current_depth+1)  -- Recursively explore nested tables
            else
                result[key] = value  -- Directly assign non-table values
            end
        end
    end

    return result
end

-- Function to collect data from the game
-- Called when a new hand is dealt
local function collect_data()
    log("Collecting data from game state...")

    local data = {
        current_round = {},
        hand = {},
        hands = {},
        used_jokers = {},
        jokers = {},
        blind = {},
        seed = "",
        round = -1,
        hands_played = -1,
        skips = -1,
        dollars = -1,
        blind_chip = -1,
        stake = "",
        chips = -1
    }

    -- Current round data
    log("Collecting current round data...")
    local current_round = {
        discards_left = G.GAME.current_round.discards_left or -1,
        hands_left = G.GAME.current_round.hands_left or -1,
    }
    table.insert(data.current_round, current_round)

    -- Hands data
    log("Collecting cards in hand...")
    for card_idx in pairs(G.hand.cards) do
        local c = G.hand.cards[card_idx]
        local card_data = {
            card_key = c.config.card_key,
            card_name = c.config.card.name,
            card_pos = c.config.center.pos.x,
            card_type = c.config.center.key,
            card_seal = c.seal or "NONE",
        }
        table.insert(data.hand, card_data)
    end

    -- Blind data
    log("Collecting blind data...")
    local blind = G.GAME.blind.config.blind or {}
    table.insert(data.blind, blind)

    local blind_chips = G.GAME.blind.chips or -1
    data.blind_chip = blind_chips

    -- Hands data
    log("Collecting hands data...")
    local hands = {}
    for h_idx in pairs(G.GAME.hands) do
        -- h_idx is the name of the hand, e.g. "Flush House"

        local h = G.GAME.hands[h_idx]
        local this_hand_data = {
            order = h.order or -1,
            level = h.level or -1,
            mult = h.mult or -1,
            chips = h.chips or -1,
            played_this_round = h.played_this_round or -1,
            played = h.played or -1,
        }

        hands[h_idx] = this_hand_data
    end
    data.hands = hands

    -- Used jokers data
    log("Collecting used_jokers...")
    local used_jokers = {}
    for _, joker in pairs(G.GAME.used_jokers) do
        table.insert(used_jokers, _)
    end
    data.used_jokers = used_jokers

    -- G.jokers data
    log("Collecting jokers data...")
    for j_idx in pairs(G.jokers.cards) do
        local j = G.jokers.cards[j_idx]
        local joker_data = {
            card_ed = j.edition or {},
            card_key = j.config.card_key,
            card_pos = j.config.center.pos.x,
            card_type = j.config.center.key,
        }    
        table.insert(data.jokers, joker_data)
    end
   
    -- G.GAME.used_jokers info
    log("Collecting used jokers info...")
    local used_jokers_info = {
        used_jokers = {
            insp = inspect(G.GAME.used_jokers)
        }
    }
    table.insert(data.used_jokers, used_jokers_info)

    -- Other data
    log("Collecting other game data...")
    data.seed = G.GAME.pseudorandom.seed or "UNKNOWN"
    data.round = G.GAME.round or -1
    data.hands_played = G.GAME.hands_played or -1
    data.skips = G.GAME.skips or -1
    data.round_scores = G.GAME.round_scores or {}
    data.dollars = G.GAME.dollars or -1
    data.stake = G.GAME.stake or ""
    data.chips = G.GAME.chips or -1

    log("Data collection complete.")
    return data
end

-- Function to send data to the server
-- This function will convert all data to a format that can be serialized to JSON, 
-- and then send it to the server 
local function send_to_server(data)
    -- Go through each field and check the type
    for key, value in pairs(data) do
        if type(value) == "table" then
            for sub_key, sub_value in pairs(value) do
                value[sub_key] = convert_type(sub_value)
            end
        else
            data[key] = convert_type(value)
        end
    end

    -- Serialize the data to JSON
    local serialized_data = json.encode(data)
    local url = "http://localhost:8080/data"

    -- Prepare the HTTP request options
    local options = {
        method = "POST",
        headers = { ["Content-Type"] = "application/json" },
        data = serialized_data
    }

    -- Send the HTTP request async so that the game doesn't freeze (hopefully)
    https.asyncRequest(url, options, function(status, body, headers)
        log("Response status: " .. status)
        log("Response body: " .. body)
        for k, v in pairs(headers) do
            log("Header: " .. k .. " = " .. v)
        end
    end)
end

-- Test function, creates some fake data to send to the server
local function send_to_server_test()
    local test_data = {
            cards = {
                {id = 1, name = "Ace of Spades"},
                {id = 2, name = "King of Hearts"}
            },
            jokers = {
                {id = 101, name = "Lucky Joker"},
                {id = 102, name = "Wild Joker"}
            },
            run_info = {
                round = 5,
                score = 12000,
                time = 42
            },
            hands = {
                {name = "Full House", level = 2, play_count = 3},
                {name = "Flush", level = 1, play_count = 7}
            }
        }
    log("Running in test mode. Test data will be sent to server")
    send_to_server(test_data)
    log("Test data sent successfully.")
end

-- Hook into the "update_selecting_hand" event
local oldgameupdateselectinghand = Game.update_selecting_hand
function Game:update_selecting_hand(dt)

    -- If the mod is not enabled, do nothing
    if not config.mod_enabled then
        log("Module is disabled. Skipping data collection.")
        return oldgameupdateselectinghand(self, dt)
    end

    if not G.STATE_COMPLETE then -- Apparently a value of G.STATE_COMPLETE greater than 1 means the game is still updating state?
        local data = collect_data()
        send_to_server(data)
    end
    -- Call the original function to ensure game logic continues as expected
    return oldgameupdateselectinghand(self, dt)
end



