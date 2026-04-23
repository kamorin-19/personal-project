declare global {
	namespace App {
		interface Locals {
			user: { userId: string; email: string; name: string | null } | null;
		}
		interface PageData {
			user?: { userId: string; email: string; name: string | null } | null;
		}
	}
}

export {};
