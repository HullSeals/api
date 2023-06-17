from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

type_defs = gql(
    """
    enum Platform {
        ODYSSEY
        XBOX
        PLAYSTATION
        LEGACY_HORIZONS
        LIVE_HORIZONS
        UNKNOWN
    }
    
    enum CaseType {
        SEAL
        BLACK
        BLUE
        FISH
    }
    
    enum Status {
        ACTIVE
        CLOSED
        DELAYED
        INACTIVE
    }
    
    type Cmdrs {
        cmdr_name: String!
        platform: Int
    }
    
    type Seal {
        name: String!
        seal_id: Int!
        case_num: Int
        cmdrs: [Cmdrs]
        irc_alias: [String]
        reg_date: String!
        dw2: Boolean
    }
    
    type KFCoords {
        x_coord: Float
        y_coord: Float
    }
    
    enum KFType {
        LIFT
        GOLF
        PUCK
        PICK
    }
    
    type Case {
        client_name: String!
        system: String!
        platform: Platform!
        board_id: Int!
        case_type: CaseType!
        creation_time: String!
        updated_time: String!
        status: Status!
        welcomed: Boolean!
        dispatchers: [Seal]
        responders: [Seal]
        case_notes: [String]
        closed_to: Seal
        irc_nick: String
        can_synth: Boolean
        o2_timer: String
        hull_percent: Int
        canopy_broken: Boolean
        planet: String
        pcoords: KFCoords
        kftype: KFType
    }
    
    type Query {
        hello: String!
    }
"""
)

# Create type instance for Query type defined in our schema...
query = QueryType()


# ...and assign our resolver function to its "hello" field.
@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
