context('Alive Tests', () => {
	it('should load the homepage', () => {
		cy.visit('/')
		cy.contains("Metalab Library").should('be.visible')
	})
})
