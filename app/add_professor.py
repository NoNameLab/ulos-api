from app.auth.hashing import get_password_hash, verify_password



print(verify_password('password', '$2b$12$Sc/Tz6ifzrptDAK2iWQIRe0E7MOKM1x9iCxHSrc0/lgpb/si8J2wG'))
print(verify_password('password', '$2b$12$ZjhJ9gR1CLbOtp9WN69qF.nqTFLvc4MxAOiLCroSbqwpn7.Bs8/d.'))
print(verify_password('password', '$2b$12$WgpH95DTdJxnHSGS0uocbOWloTOjxMFjwGgt7FZuRRh/whkjKn7F2'))
