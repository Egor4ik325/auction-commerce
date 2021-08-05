# Un_i_direct_ional | Bi_direct_ional

- Directional
- Idirectional = Bidirectional
- Unidirectional

## Relations

- ManyToOne (M:1)   - PK/FK relation
- OneToMany (1:M)   - no SQL (reversed M:1)
- ManyToMany (M:M)  - no SQL (M:1 and 1:M in join table)
- OneToOne (1:1)    - no SQL (M unique constrains in M:1)

- ForeignKey (M:1)  - Unidirectional (only 1 direction) + related_name (1:M) (Bidirectional)
- ManyToMany (M:M)  - RelatedManager = Field + related_name (Bidirectional)
- OneToOne  (1:1)   - ForeignKey(unique=True)

- RelatedManager
- ManyRelatedManager

* Django relations  - Uniderectional   
* related_name      - Bidirectional

## Bidirectional (1:M)

State:
    * PK
    - cities FK (1:M)   - collection property
City:
    * PK
    - state FK (M:1)    - property

> Django: ForeignKey + related_name (M:1 or 1:M reverse)

## Unidirectinal (M:M)

Bus:
    * PK
    - riders FK (M:M) - all riders ridden
Rider:
    * PK

## Bidirectional (M:M)

Person:
    * PK
    - friends FK (M:M) -> Person