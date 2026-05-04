from pydantic import BaseModel, Field


class ExpenseCategoryCreate(BaseModel):
	category_name: str = Field(min_length=1, max_length=50)
	color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
	icon_emoji: str = Field(min_length=1, max_length=2)


class ExpenseCategoryUpdate(BaseModel):
	category_name: str | None = Field(default=None, min_length=1, max_length=50)
	color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
	icon_emoji: str | None = Field(default=None, min_length=1, max_length=2)


class ExpenseCategoryResponse(BaseModel):
	category_id: str
	category_name: str
	color: str
	icon_emoji: str
	created_at: str
	updated_at: str

	@classmethod
	def from_dynamo(cls, item: dict) -> "ExpenseCategoryResponse":
		return cls(
			category_id=item["categoryId"],
			category_name=item["categoryName"],
			color=item["color"],
			icon_emoji=item["iconEmoji"],
			created_at=item["createdAt"],
			updated_at=item["updatedAt"],
		)


class ExpenseCategoryListResponse(BaseModel):
	items: list[ExpenseCategoryResponse]
