# Invoice Manager
Invoice module for [AllianceAuth](https://gitlab.com/allianceauth/allianceauth) with simplicity and extendability in mind. 

Included `Bits and Bobs`:
 * Simple Invoice Model
   * Assigned to Character
   * Due Dates
   * Invoice Ref used for tracking payments
   * Notifications
 * Simple task for checking for payments

 The `ToDo` List:
  * Make Payment Corp selectable at invoice level
  * Add the copy `Ref` and Open info in game from SRP Mod

## Permissions
There are some basic access perms

Admin perms are filtered by main character, if a person has neutral alts loaded their invoices will also be visible to someone who can see their main.

 Perm | Admin Site	 | Perm | Description
 --- | --- | --- | ---
 access_invoices | nill | Can Access the Invoice App. | Generic Access perm to show the Invoice menu option
 view_all | nill | Can View All Invoices. | Superuser level access
 view_alliance | nill | Can View Own Alliances Invoices. | Alliance only level access
 view_corp | nill | Can View Own Corps Invoices. | Corp restricted level access
