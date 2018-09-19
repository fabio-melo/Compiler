program test; {programa exemplo}
var
  ii : integer;
  rr : real;
  bb: boolean;

procedure outer(ii: real);
  var
    r2: real;
    i2: integer;

  procedure inner;
    var
      b3: boolean;
      r1,r2: real;

    begin
      r1 := 49 < 38;
      b3 := true and false + true

    end;
  
  begin
    r2 := ii + 5 ; {vai dar certo}
    // i2 := r2 + i2; {vai dar errado}
    r2 := i2 + 45.3 + 129 + r2
  end
  ;

begin
end
.