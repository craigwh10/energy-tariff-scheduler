<details><summary>How do I get my account number & API key?</summary>
<p>
Go to <a href="https://octopus.energy" target="_blank">octopus.energy</a> and sign in, then follow these steps after clicking the menu button on the home page.
</p>
<img src="../../01-menu.png" alt="clicking the menu navigation in the top left, then navigating to my account"></img>

<img src="../../02-acc-no.png" alt="image showing that you should copy the account number from the field under your name, and then selecting personal details under it to get to next step "></img>

<img src="../../03-apikey01.png" alt="after clicking personal details, you should scroll down to developer settings and then click API access"></img>

<img src="../../04-apikey02.png" alt="then copy the API key that is in the field, this should read like some nonsense characters"></img>

<p style="font-weight: bold;">A best practice is to place these in a <code>.env</code> file, and bring them in with <code>python-dotenv</code>, be sure to put <code>.env</code> in a <code>.gitignore</code> file.</p>

</details>