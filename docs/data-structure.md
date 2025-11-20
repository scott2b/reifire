# Reifire data specification

## Specification goals

The Reifire data spec is intended to model the process illustrated in reification.aka.ms.nfw.2024.png
which is taken from page 28 of the [Microsoft New Future of Work Report 2024](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/NFWReport2024_12.20.24.pdf)

The goals of this specification are to:

 - model the artifacts of prompt reification including content types, objects, aspects, etc.
 - provide a complete data model in reified form that can be articulated into natural language form
 - model visualizations and visualization alternatives to facilitate UI builds and integrations
 - model user interactions and workflows that involve:

    * the reification of prompts into object representations
    * the manipulation of reified components into new forms such as creating theme, attribute, or object variations
    * the articulation of reified forms into natural language prompts


The Reifire library handles most of the heavy lifting of reification and articulation through
sensible defaults, but is also highly customizable. The following data specification defines
the reified representations and their relationships to articulated form via parsings,
mappings, conversions, de/serializations, lookups, etc.

## The specification

### 1. Core Data Structure

The root reification object is a JSON object with the following top-level components:

```json
{
    "object": Object,
    "type": Type,
    "artifact": Artifact,
    "metadata": Metadata
}
```

### 2. Component Definitions

#### 2.1 Object Component
Represents the primary subject with its intrinsic modifiers:
```json
{
    "name": string,
    "modifiers": [Modifier],
    "description": string,
    "variants": [Object],
    "properties": {
        string: any
    }
}
```

#### 2.2 Modifier Component
Represents intrinsic modifications to the object itself:
```json
{
    "name": string,
    "value": any,
    "category": string,
    "alternatives": [Modifier],
    "properties": {
        string: any
    }
}
```

#### 2.3 Type Component
Defines the category or form of the output artifact:
```json
{
    "name": string,
    "category": string,  // e.g., "visual", "textual", "interactive"
    "properties": {
        string: any
    }
}
```

#### 2.4 Artifact Component
Defines the output representation and its attributes:
```json
{
    "type": string,      // e.g., "image", "text", "qa", "code"
    "attributes": [ArtifactAttribute],
    "visualization": Visualization,
    "relationships": [Relationship],
    "properties": {
        string: any
    }
}
```

#### 2.5 ArtifactAttribute Component
Represents characteristics of the output artifact:
```json
{
    "name": string,
    "value": any,
    "category": string,
    "visualization": Visualization,
    "alternatives": [ArtifactAttribute],
    "properties": {
        string: any
    }
}
```

#### 2.6 Visualization Component
Defines how components are visually represented:
```json
{
    "source": string,
    "name": string,
    "image": string,
    "images": [string],
    "attribution": string,
    "alternatives": [Visualization],
    "properties": {
        string: any
    }
}
```

#### 2.7 Metadata Component
Contains information about the reification process:
```json
{
    "timestamp": string,
    "version": string,
    "original_prompt": string,
    "processing_info": {
        string: any
    }
}
```

### 3. Visualization Sources

The specification supports multiple visualization sources:

- **COLORS**: Color blocks and schemes
- **NOUNPROJECT**: Icons and symbols from the Noun Project
- **OPENAI**: Generated images
- **CUSTOM**: User-defined visualization sources

### 4. Component Relationships

Components can be related through:

1. **Hierarchical relationships**
   - Parent-child relationships between objects
   - Type-subtype relationships
   - Attribute groupings

2. **Semantic relationships**
   - Object-attribute associations
   - Type-attribute constraints
   - Cross-component references

3. **Visual relationships**
   - Layout constraints
   - Visual hierarchy
   - Compositional rules

### 5. Interaction Models

The specification supports these key interactions:

1. **Component Manipulation**
```json
{
    "action": string,
    "target": string,
    "parameters": {
        string: any
    }
}
```

2. **State Transitions**
```json
{
    "from_state": string,
    "to_state": string,
    "trigger": string,
    "conditions": {
        string: any
    }
}
```

### 6. Articulation Rules

Rules for converting reified form back to natural language:

1. **Component Order**
   - Type precedes object
   - Attributes follow object
   - Relationships are expressed last

2. **Natural Language Templates**
```json
{
    "template": string,
    "variables": {
        string: string
    },
    "conditions": {
        string: any
    }
}
```

### 7. Extension Points

The specification can be extended through:

1. **Custom Components**
   - User-defined component types
   - Custom visualization sources
   - Extended metadata fields

2. **Plugin Architecture**
```json
{
    "plugin_name": string,
    "version": string,
    "components": [string],
    "handlers": {
        string: string
    }
}
```

### 8. Examples

#### Basic Illustration Example
```json
{
    "object": {
        "name": "Cthulu",
        "modifiers": [
            {
                "name": "age",
                "value": "baby",
                "alternatives": [
                    {
                        "name": "age",
                        "value": "adult"
                    }
                ]
            }
        ]
    },
    "type": {
        "name": "illustration",
        "category": "visual"
    },
    "artifact": {
        "type": "image",
        "attributes": [
            {
                "name": "style",
                "value": "children's illustration",
                "visualization": {
                    "source": "nounproject",
                    "name": "children art",
                    "image": "children_art.svg"
                }
            },
            {
                "name": "mood",
                "value": "scary-cute"
            },
            {
                "name": "color scheme",
                "visualization": {
                    "source": "colors",
                    "name": "brown-green-purple",
                    "images": [
                        "brown.svg",
                        "green.svg",
                        "purple.svg"
                    ]
                }
            }
        ],
        "visualization": {
            "source": "openai",
            "name": "baby cthulu",
            "image": "bc.png"
        }
    },
    "metadata": {
        "timestamp": "2024-01-20T10:00:00Z",
        "version": "1.0",
        "original_prompt": "Scary-cute baby Cthulu illustration with brown-green-purple color scheme. Wide outlines, childrens illustration style."
    }
}
```

#### Question-Answer Example
```json
{
    "object": {
        "name": "photosynthesis",
        "modifiers": [
            {
                "name": "scope",
                "value": "process"
            }
        ]
    },
    "type": {
        "name": "explanation",
        "category": "textual"
    },
    "artifact": {
        "type": "qa",
        "attributes": [
            {
                "name": "complexity",
                "value": "elementary"
            },
            {
                "name": "format",
                "value": "step-by-step"
            },
            {
                "name": "tone",
                "value": "educational"
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T11:00:00Z",
        "version": "1.0",
        "original_prompt": "Explain the process of photosynthesis in simple steps for elementary students."
    }
}
```

#### Code Generation Example
```json
{
    "object": {
        "name": "authentication",
        "modifiers": [
            {
                "name": "type",
                "value": "oauth2",
                "alternatives": [
                    {
                        "name": "type",
                        "value": "jwt"
                    }
                ]
            },
            {
                "name": "scope",
                "value": "middleware"
            }
        ]
    },
    "type": {
        "name": "implementation",
        "category": "code"
    },
    "artifact": {
        "type": "code",
        "attributes": [
            {
                "name": "language",
                "value": "python",
                "alternatives": [
                    {
                        "name": "language",
                        "value": "typescript"
                    }
                ]
            },
            {
                "name": "framework",
                "value": "fastapi"
            },
            {
                "name": "style",
                "value": "functional"
            },
            {
                "name": "documentation",
                "value": "detailed"
            }
        ],
        "relationships": [
            {
                "type": "depends_on",
                "source": "middleware",
                "target": "user_model",
                "properties": {
                    "type": "import"
                }
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T12:00:00Z",
        "version": "1.0",
        "original_prompt": "Create a FastAPI OAuth2 authentication middleware with detailed documentation using functional programming style."
    }
}
```

#### Complex Visual Scene Example
```json
{
    "object": {
        "name": "cityscape",
        "modifiers": [
            {
                "name": "time_period",
                "value": "future",
                "alternatives": [
                    {
                        "name": "time_period",
                        "value": "present"
                    }
                ]
            },
            {
                "name": "location",
                "value": "tokyo"
            }
        ]
    },
    "type": {
        "name": "scene",
        "category": "visual"
    },
    "artifact": {
        "type": "image",
        "attributes": [
            {
                "name": "style",
                "value": "cyberpunk",
                "visualization": {
                    "source": "nounproject",
                    "name": "cyberpunk",
                    "image": "cyberpunk_style.svg"
                }
            },
            {
                "name": "time",
                "value": "night"
            },
            {
                "name": "weather",
                "value": "rain"
            },
            {
                "name": "composition",
                "value": "street level view"
            }
        ],
        "visualization": {
            "source": "openai",
            "name": "future_tokyo_night",
            "image": "tokyo_cyber.png"
        },
        "relationships": [
            {
                "type": "contains",
                "source": "scene",
                "target": "neon_signs",
                "properties": {
                    "position": "throughout"
                }
            },
            {
                "type": "contains",
                "source": "scene",
                "target": "flying_vehicles",
                "properties": {
                    "position": "sky"
                }
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T13:00:00Z",
        "version": "1.0",
        "original_prompt": "Create a rainy night scene of futuristic Tokyo in cyberpunk style, viewed from street level with neon signs and flying vehicles."
    }
}
```

#### Data Analysis Query Example
```json
{
    "object": {
        "name": "sales_data",
        "modifiers": [
            {
                "name": "time_range",
                "value": "last_quarter",
                "alternatives": [
                    {
                        "name": "time_range",
                        "value": "last_year"
                    }
                ]
            },
            {
                "name": "region",
                "value": "north_america"
            }
        ]
    },
    "type": {
        "name": "analysis",
        "category": "data"
    },
    "artifact": {
        "type": "query",
        "attributes": [
            {
                "name": "operation",
                "value": "aggregation"
            },
            {
                "name": "grouping",
                "value": ["product_category", "month"]
            },
            {
                "name": "metrics",
                "value": ["revenue", "growth_rate"]
            },
            {
                "name": "format",
                "value": "sql"
            }
        ],
        "relationships": [
            {
                "type": "references",
                "source": "sales_data",
                "target": "product_catalog",
                "properties": {
                    "join_type": "left"
                }
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T14:00:00Z",
        "version": "1.0",
        "original_prompt": "Generate a SQL query to analyze last quarter's North American sales data, showing revenue and growth rate by product category and month."
    }
}
```

#### Interactive UI Component Example
```json
{
    "object": {
        "name": "date_picker",
        "modifiers": [
            {
                "name": "range",
                "value": "multi",
                "alternatives": [
                    {
                        "name": "range",
                        "value": "single"
                    }
                ]
            },
            {
                "name": "scope",
                "value": "calendar"
            }
        ]
    },
    "type": {
        "name": "component",
        "category": "interactive"
    },
    "artifact": {
        "type": "ui_element",
        "attributes": [
            {
                "name": "framework",
                "value": "react"
            },
            {
                "name": "style_system",
                "value": "tailwind"
            },
            {
                "name": "theme",
                "value": "dark",
                "alternatives": [
                    {
                        "name": "theme",
                        "value": "light"
                    }
                ]
            },
            {
                "name": "accessibility",
                "value": "wcag_aa"
            }
        ],
        "relationships": [
            {
                "type": "contains",
                "source": "date_picker",
                "target": "calendar_grid",
                "properties": {
                    "interaction": "clickable"
                }
            },
            {
                "type": "contains",
                "source": "date_picker",
                "target": "time_selector",
                "properties": {
                    "optional": true
                }
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T15:00:00Z",
        "version": "1.0",
        "original_prompt": "Create a WCAG AA compliant React date range picker component with dark theme using Tailwind CSS."
    }
}
```

#### Natural Language Generation Example
```json
{
    "object": {
        "name": "product_review",
        "modifiers": [
            {
                "name": "product",
                "value": "smartphone",
                "properties": {
                    "brand": "Apple",
                    "model": "iPhone 15 Pro"
                }
            },
            {
                "name": "experience",
                "value": "long_term",
                "alternatives": [
                    {
                        "name": "experience",
                        "value": "first_impression"
                    }
                ]
            }
        ]
    },
    "type": {
        "name": "content",
        "category": "textual"
    },
    "artifact": {
        "type": "article",
        "attributes": [
            {
                "name": "tone",
                "value": "professional",
                "alternatives": [
                    {
                        "name": "tone",
                        "value": "casual"
                    }
                ]
            },
            {
                "name": "perspective",
                "value": "expert"
            },
            {
                "name": "structure",
                "value": "sections",
                "properties": {
                    "sections": [
                        "design",
                        "performance",
                        "camera",
                        "battery",
                        "verdict"
                    ]
                }
            },
            {
                "name": "word_count",
                "value": 2000
            }
        ],
        "relationships": [
            {
                "type": "references",
                "source": "review",
                "target": "technical_specs",
                "properties": {
                    "validation": "required"
                }
            },
            {
                "type": "compares",
                "source": "iphone_15_pro",
                "target": "iphone_14_pro",
                "properties": {
                    "aspects": ["performance", "camera"]
                }
            }
        ]
    },
    "metadata": {
        "timestamp": "2024-01-20T16:00:00Z",
        "version": "1.0",
        "original_prompt": "Write a comprehensive 2000-word professional review of the iPhone 15 Pro based on long-term usage, including comparisons with the previous model."
    }
}
```
