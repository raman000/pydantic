from __future__ import annotations as _annotations

from typing import TYPE_CHECKING, Any, Union

from pydantic_core import core_schema

if TYPE_CHECKING:
    from ..json_schema import JsonSchemaMode, JsonSchemaValue

    CoreSchemaOrField = Union[
        core_schema.CoreSchema,
        core_schema.ModelField,
        core_schema.DataclassField,
        core_schema.TypedDictField,
        core_schema.ComputedField,
    ]

__all__ = 'GetJsonSchemaHandler', 'GetCoreSchemaHandler'


class GetJsonSchemaHandler:
    """Handler to call into the next JSON schema generation function.

    Attributes:
        mode: Json schema mode, can be `validation` or `serialization`.
    """

    mode: JsonSchemaMode

    def __call__(self, __core_schema: CoreSchemaOrField) -> JsonSchemaValue:
        """Call the inner handler and get the JsonSchemaValue it returns.
        This will call the next JSON schema modifying function up until it calls
        into `pydantic.json_schema.GenerateJsonSchema`, which will raise a
        `pydantic.errors.PydanticInvalidForJsonSchema` error if it cannot generate
        a JSON schema.

        Args:
            __core_schema: A `pydantic_core.core_schema.CoreSchema`.

        Returns:
            JsonSchemaValue: The JSON schema generated by the inner JSON schema modify
            functions.
        """
        raise NotImplementedError

    def resolve_ref_schema(self, __maybe_ref_json_schema: JsonSchemaValue) -> JsonSchemaValue:
        """Get the real schema for a `{"$ref": ...}` schema.
        If the schema given is not a `$ref` schema, it will be returned as is.
        This means you don't have to check before calling this function.

        Args:
            __maybe_ref_json_schema: A JsonSchemaValue, ref based or not.

        Raises:
            LookupError: If the ref is not found.

        Returns:
            JsonSchemaValue: A JsonSchemaValue that has no `$ref`.
        """
        raise NotImplementedError


class GetCoreSchemaHandler:
    """Handler to call into the next CoreSchema schema generation function."""

    def __call__(self, __source_type: Any) -> core_schema.CoreSchema:
        """Call the inner handler and get the CoreSchema it returns.
        This will call the next CoreSchema modifying function up until it calls
        into Pydantic's internal schema generation machinery, which will raise a
        `pydantic.errors.PydanticSchemaGenerationError` error if it cannot generate
        a CoreSchema for the given source type.

        Args:
            __source_type: The input type.

        Returns:
            CoreSchema: The `pydantic-core` CoreSchema generated.
        """
        raise NotImplementedError

    def generate_schema(self, __source_type: Any) -> core_schema.CoreSchema:
        """Generate a schema unrelated to the current context.
        Use this function if e.g. you are handling schema generation for a sequence
        and want to generate a schema for its items.
        Otherwise, you may end up doing something like applying a `min_length` constraint
        that was intended for the sequence itself to it's items!

        Args:
            __source_type: The input type.

        Returns:
            CoreSchema: The `pydantic-core` CoreSchema generated.
        """
        raise NotImplementedError

    def resolve_ref_schema(self, __maybe_ref_schema: core_schema.CoreSchema) -> core_schema.CoreSchema:
        """Get the real schema for a `definition-ref` schema.
        If the schema given is not a `definition-ref` schema, it will be returned as is.
        This means you don't have to check before calling this function.

        Args:
            __maybe_ref_schema: A `CoreSchema`, `ref`-based or not.

        Raises:
            LookupError: If the `ref` is not found.

        Returns:
            A concrete `CoreSchema`.
        """
        raise NotImplementedError