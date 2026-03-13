import { apiRequest } from "@/src/services/api";
import type { RegisterAttendeePayload, Registration } from "@/src/types/attendee.types";

export const attendeeService = {
	async getEventAttendees(eventId: number, token: string): Promise<Registration[]> {
		const response = await apiRequest<Registration[]>(`/attendees/event/${eventId}`, {
			method: "GET",
			token,
		});

		return response.data;
	},

	async registerToEvent(eventId: number, payload: RegisterAttendeePayload, token: string): Promise<Registration> {
		const response = await apiRequest<Registration>(`/attendees/event/${eventId}/register`, {
			method: "POST",
			body: payload,
			token,
		});

		return response.data;
	},

	async cancelRegistration(registrationId: number, token: string): Promise<Registration> {
		const response = await apiRequest<Registration>(`/attendees/registration/${registrationId}/cancel`, {
			method: "PATCH",
			token,
		});

		return response.data;
	},
};
