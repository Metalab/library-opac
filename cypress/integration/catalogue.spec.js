context('Catalogue Tests', () => {
	it('should load the "Hauptstelle" page', () => {
		cy.visit('location_HauptstelleMetalab.html')
		cy.get('.listItem').should('have.length.at.least', 10)
	})
})
