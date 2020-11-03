context('Alive Tests', () => {
	it('should open the homepage', () => {
		cy.visit('/')
		cy.contains("Metalab Library").should('be.visible')
	})
})
