The Personal store is holding leftovers from the earlier PowerShell round — the cleanup step never ran on this box. Look at the expiry dates, they give it away:

Cert	Expires	Which round
WEC-Marcin-1	19/08/2031	Old PowerShell
WEC-Marcin-1	20/08/2031	New openssl ✓
WEC-Marcin-2	20/08/2031	Shouldn't be here at all
WEF-Lab-RootCA	20/08/2036	Old PowerShell
WEF-Lab-RootCA	21/08/2036	The one accidentally generated mid-session
WEF-Marcin	20/08/2031	Old client cert, wrong CN

Two other problems visible:

Your third import went to the wrong file. The console shows WEF-Marcin.cer imported into TrustedPeople with thumbprint 5CCD3042628151B34DC0C94196A54FE45C73BE1E and subject CN=WEF-Marcin — that's the old client cert. You want WEF-Marcin-1.cer, thumbprint B538B862..., subject CN=WEF-Marcin-1. The mapping expects CN=WEF-Marcin-1, so this won't work as imported.

Two root CAs in Personal. Root CAs belong in Root, not My — these are residue from running New-SelfSignedCertificate on this machine, which also left their private keys here. Anyone with local admin could mint certs your collectors trust.

Clean up
powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|WEC-Marcin|WEF-Marcin"} |
  Select-Object PSParentPath, Subject, Thumbprint, NotAfter | Format-Table -AutoSize

Remove everything that isn't one of your three expected thumbprints:

powershell
$keep = @(
  "2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA",
  "B320815C2A34A8AC14588F01C6E6A601A41CB490",
  "B538B86224DD8B465DF236AA14F2A2CE44A97027"
)
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|WEC-Marcin|WEF-Marcin" -and $_.Thumbprint -notin $keep} |
  Remove-Item
Import the correct client cert
powershell
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Note the -1 — that's the file you need, not WEF-Marcin.cer.

Verify — exactly three, nothing else
powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object PSParentPath, Subject, Thumbprint | Format-Table -AutoSize

Expect 2CFBC70E... in Root, B320815C... in My, B538B862... in TrustedPeople. Only then run the listener bind and the mapping.

Also worth checking C:\WEF-Certs\ on this box — if both WEF-Marcin.cer and WEF-Marcin-1.cer are sitting there, delete the old one so you can't grab the wrong file again.

before next steps how to validate if i have requried certificates

First, note the two stragglers at the bottom — WEF-Marcin.cer and WEF-Marcin.pfx, dated 20/08 17:25 rather than 21/08 11:28. Those are the old PowerShell client cert, and they're what got imported by mistake earlier. Delete them so you can't pick the wrong file again:

powershell
Remove-Item C:\WEF-Certs\WEF-Marcin.cer, C:\WEF-Certs\WEF-Marcin.pfx

Also worth knowing this box has RootCA.key sitting in it — the CA private key. Fine while you're building, but it shouldn't live on a collector long-term.

Validate what's in the certificate stores

Run this on whichever machine you're checking. It compares what's installed against what should be there:

powershell
$expected = @{
  "2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA" = "RootCA"
  "B320815C2A34A8AC14588F01C6E6A601A41CB490" = "WEC-Marcin-1"
  "EE81D9A17D5B4C7C55CC14F77F8ED4A996A95418" = "WEC-Marcin-2"
  "B538B86224DD8B465DF236AA14F2A2CE44A97027" = "WEF-Marcin-1"
}

Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object @{n='Store';e={$_.PSParentPath -replace '.*\\',''}},
                Subject, Thumbprint,
                @{n='Status';e={ if ($expected.ContainsKey($_.Thumbprint)) {"OK - $($expected[$_.Thumbprint])"} else {"STALE - remove"} }} |
  Format-Table -AutoSize
What each machine should show

WEC-Marcin-1 — exactly three rows:

Store	Subject	Thumbprint
Root	CN=WEF-Lab-RootCA	2CFBC70E…
My	CN=WEC-Marcin-1	B320815C…
TrustedPeople	CN=WEF-Marcin-1	B538B862…

WEC-Marcin-2 — same, but CN=WEC-Marcin-2 / EE81D9A1… in My.

WEF-Marcin-1 — two rows:

Store	Subject	Thumbprint
Root	CN=WEF-Lab-RootCA	2CFBC70E…
My	CN=WEF-Marcin-1	B538B862…

Anything showing STALE - remove gets deleted:

powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin" -and $_.Thumbprint -notin $expected.Keys} |
  Remove-Item
Two further checks worth doing

Chain validation — proves the cert actually verifies against the installed root, not just that both are present:

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -match "Marcin"} | ForEach-Object {
  $chain = New-Object System.Security.Cryptography.X509Certificates.X509Chain
  $ok = $chain.Build($_)
  "{0,-20} ChainValid={1}" -f $_.Subject, $ok
}

Private key present and accessible — the most common silent failure:

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -match "Marcin"} |
  Select-Object Subject, HasPrivateKey, Thumbprint

HasPrivateKey must be True. If it's False, the .pfx import didn't take properly and you'd need to reimport. This is separate from the NETWORK SERVICE permission — that one you still need to grant via certlm.msc, and it won't show up in any of the checks above.
