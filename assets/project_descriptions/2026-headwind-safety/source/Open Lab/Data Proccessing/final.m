clear; clc;

dragscalingfactor  = 12.52;
liftscalingfactor  = 89.49;
dragscalingfactor2 = 12.47;
liftscalingfactor2 = 72.48;

toolUncertainty = 0.01;   % N

data150    = readmatrix('150deg.xlsx');
data165    = readmatrix('165deg.xlsx');
data180    = readmatrix('180deg.xlsx');
datastand  = readmatrix('teststand1data.xlsx');
datastand2 = readmatrix('teststand2data.xlsx');

area150 = 5.02682e-3;
area165 = 5.28867e-3;
area180 = 5.37630e-3;

n = 10;                  % samples per point
t95 = 2.262;             % 95% t critical for df = 9

vel150     = data150(:,2);
drag150    = data150(:,3);
dragstd150 = data150(:,4);
lift150    = data150(:,5);
liftstd150 = data150(:,6);

vel165     = data165(:,2);
drag165    = data165(:,3);
dragstd165 = data165(:,4);
lift165    = data165(:,5);
liftstd165 = data165(:,6);

vel180     = data180(:,2);
drag180    = data180(:,3);
dragstd180 = data180(:,4);
lift180    = data180(:,5);
liftstd180 = data180(:,6);

velstand      = datastand(:,2);
dragstand     = datastand(:,3);
dragstdstand  = datastand(:,4);
liftstand     = datastand(:,5);
liftstdstand  = datastand(:,6);

velstand2     = datastand2(:,2);
dragstand2    = datastand2(:,3);
dragstdstand2 = datastand2(:,4);
liftstand2    = datastand2(:,5);
liftstdstand2 = datastand2(:,6);

% Force calculations
forcedrag165 = zeros(length(drag165),1);
forcelift165 = zeros(length(lift165),1);
forcedrag180 = zeros(length(drag180),1);
forcelift180 = zeros(length(lift180),1);
forcedrag150 = zeros(length(drag150),1);
forcelift150 = zeros(length(lift150),1);

for i = 1:length(vel165)
    forcedrag165(i) = dragscalingfactor * ((drag165(i) - drag165(1)) - (dragstand(i) - dragstand(1)));
    forcelift165(i) = liftscalingfactor * ((lift165(i) - lift165(1)) - (liftstand(i) - liftstand(1)));
end

for i = 1:length(vel180)
    forcedrag180(i) = dragscalingfactor * ((drag180(i) - drag180(1)) - (dragstand(i) - dragstand(1)));
    forcelift180(i) = liftscalingfactor * ((lift180(i) - lift180(1)) - (liftstand(i) - liftstand(1)));
end

for i = 1:length(vel150)
    forcedrag150(i) = dragscalingfactor2 * ((drag150(i) - drag150(1)) - (dragstand2(i) - dragstand2(1)));
    forcelift150(i) = liftscalingfactor2 * ((lift150(i) - lift150(1)) - (liftstand2(i) - liftstand2(1)));
end

% 95% confidence interval in FORCE
% For quantity: (test_i - test_1) - (stand_i - stand_1)
% standard error = sqrt(sd_test_i^2/n + sd_test_1^2/n + sd_stand_i^2/n + sd_stand_1^2/n)

dragCIforce150 = zeros(length(drag150),1);
liftCIforce150 = zeros(length(lift150),1);
dragCIforce165 = zeros(length(drag165),1);
liftCIforce165 = zeros(length(lift165),1);
dragCIforce180 = zeros(length(drag180),1);
liftCIforce180 = zeros(length(lift180),1);

for i = 1:length(vel150)
    se_drag_150 = sqrt((dragstd150(i)^2 + dragstd150(1)^2 + dragstdstand2(i)^2 + dragstdstand2(1)^2) / n);
    se_lift_150 = sqrt((liftstd150(i)^2 + liftstd150(1)^2 + liftstdstand2(i)^2 + liftstdstand2(1)^2) / n);
    dragCIforce150(i) = sqrt((t95 * dragscalingfactor2 * se_drag_150)^2 + toolUncertainty^2);
    liftCIforce150(i) = sqrt((t95 * liftscalingfactor2 * se_lift_150)^2 + toolUncertainty^2);
end

for i = 1:length(vel165)
    se_drag_165 = sqrt((dragstd165(i)^2 + dragstd165(1)^2 + dragstdstand(i)^2 + dragstdstand(1)^2) / n);
    se_lift_165 = sqrt((liftstd165(i)^2 + liftstd165(1)^2 + liftstdstand(i)^2 + liftstdstand(1)^2) / n);
    dragCIforce165(i) = sqrt((t95 * dragscalingfactor * se_drag_165)^2 + toolUncertainty^2);
    liftCIforce165(i) = sqrt((t95 * liftscalingfactor * se_lift_165)^2 + toolUncertainty^2);
end

for i = 1:length(vel180)
    se_drag_180 = sqrt((dragstd180(i)^2 + dragstd180(1)^2 + dragstdstand(i)^2 + dragstdstand(1)^2) / n);
    se_lift_180 = sqrt((liftstd180(i)^2 + liftstd180(1)^2 + liftstdstand(i)^2 + liftstdstand(1)^2) / n);
    dragCIforce180(i) = sqrt((t95 * dragscalingfactor * se_drag_180)^2 + toolUncertainty^2);
    liftCIforce180(i) = sqrt((t95 * liftscalingfactor * se_lift_180)^2 + toolUncertainty^2);
end

% Coefficients
cd150 = zeros(length(forcedrag150),1);
cl150 = zeros(length(forcelift150),1);
cd165 = zeros(length(forcedrag165),1);
cl165 = zeros(length(forcelift165),1);
cd180 = zeros(length(forcedrag180),1);
cl180 = zeros(length(forcelift180),1);

cdCI150 = zeros(length(forcedrag150),1);
clCI150 = zeros(length(forcelift150),1);
cdCI165 = zeros(length(forcedrag165),1);
clCI165 = zeros(length(forcelift165),1);
cdCI180 = zeros(length(forcedrag180),1);
clCI180 = zeros(length(forcelift180),1);

p1 = 1.184;
p2 = 1.176;

for i = 1:length(forcedrag150)
    if vel150(i) == 0
        cd150(i)   = NaN;
        cl150(i)   = NaN;
        cdCI150(i) = NaN;
        clCI150(i) = NaN;
    else
        denom150   = p2 * vel150(i)^2 * area150;
        cd150(i)   = 2 * forcedrag150(i) / denom150;
        cl150(i)   = 2 * forcelift150(i) / denom150;
        cdCI150(i) = 2 * dragCIforce150(i) / denom150;
        clCI150(i) = 2 * liftCIforce150(i) / denom150;
    end

    if vel165(i) == 0
        cd165(i)   = NaN;
        cl165(i)   = NaN;
        cdCI165(i) = NaN;
        clCI165(i) = NaN;
    else
        denom165   = p1 * vel165(i)^2 * area165;
        cd165(i)   = 2 * forcedrag165(i) / denom165;
        cl165(i)   = 2 * forcelift165(i) / denom165;
        cdCI165(i) = 2 * dragCIforce165(i) / denom165;
        clCI165(i) = 2 * liftCIforce165(i) / denom165;
    end

    if vel180(i) == 0
        cd180(i)   = NaN;
        cl180(i)   = NaN;
        cdCI180(i) = NaN;
        clCI180(i) = NaN;
    else
        denom180   = p1 * vel180(i)^2 * area180;
        cd180(i)   = 2 * forcedrag180(i) / denom180;
        cl180(i)   = 2 * forcelift180(i) / denom180;
        cdCI180(i) = 2 * dragCIforce180(i) / denom180;
        clCI180(i) = 2 * liftCIforce180(i) / denom180;
    end
end

L180 = 0.1743;
L165 = 0.17096;
L150 = 0.16245;

Re150 = vel150 * L150 / (1.55e-5);
Re165 = vel165 * L165 / (1.54e-5);
Re180 = vel180 * L180 / (1.54e-5);

% Drag coefficient plot with 95% CI error bars
figure;
errorbar(Re150, cd150, cdCI150, '-o', 'LineWidth', 1.2, 'CapSize', 6);
hold on;
errorbar(Re165, cd165, cdCI165, '-o', 'LineWidth', 1.2, 'CapSize', 6);
errorbar(Re180, cd180, cdCI180, '-o', 'LineWidth', 1.2, 'CapSize', 6);
legend('150 Degree Bend', '165 Degree Bend', '180 Degree Bend', 'Location', 'best');
xlabel('Reynolds Number');
ylabel('Drag Coefficient');
title('Drag Coefficient vs Reynolds Number for Varying Hip Bend Angles');
grid on;

% Lift coefficient plot with 95% CI error bars
figure;
errorbar(Re150, cl150, clCI150, '-o', 'LineWidth', 1.2, 'CapSize', 6);
hold on;
errorbar(Re165, cl165, clCI165, '-o', 'LineWidth', 1.2, 'CapSize', 6);
errorbar(Re180, cl180, clCI180, '-o', 'LineWidth', 1.2, 'CapSize', 6);
legend('150 Degree Bend', '165 Degree Bend', '180 Degree Bend', 'Location', 'best');
xlabel('Reynolds Number');
ylabel('Lift Coefficient');
title('Lift Coefficient vs Reynolds Number for Varying Hip Bend Angles');
grid on;

%% Human-scale wind force prediction using saturating Cd and Cl equations

% Human is 10x model length scale
scale = 10;

Lhuman150 = scale * L150;
Lhuman165 = scale * L165;
Lhuman180 = scale * L180;

Ahuman150 = scale^2 * area150;
Ahuman165 = scale^2 * area165;
Ahuman180 = scale^2 * area180;

rhoHuman = 1.184;      % kg/m^3, use same air density assumption
nuHuman  = 1.54e-5;    % m^2/s

% Wind speed range for human prediction
Vhuman = linspace(0, 35, 200);   % m/s

% Fit saturating coefficient equations
dragFit150 = fitSaturatingCoeff(Re150, cd150);
dragFit165 = fitSaturatingCoeff(Re165, cd165);
dragFit180 = fitSaturatingCoeff(Re180, cd180);

liftFit150 = fitSaturatingCoeff(Re150, cl150);
liftFit165 = fitSaturatingCoeff(Re165, cl165);
liftFit180 = fitSaturatingCoeff(Re180, cl180);

% Human Reynolds numbers
ReHuman150 = Vhuman * Lhuman150 / nuHuman;
ReHuman165 = Vhuman * Lhuman165 / nuHuman;
ReHuman180 = Vhuman * Lhuman180 / nuHuman;

% Human Cd and Cl from fitted equations
CdHuman150 = evalSaturatingCoeff(dragFit150, ReHuman150);
CdHuman165 = evalSaturatingCoeff(dragFit165, ReHuman165);
CdHuman180 = evalSaturatingCoeff(dragFit180, ReHuman180);

ClHuman150 = evalSaturatingCoeff(liftFit150, ReHuman150);
ClHuman165 = evalSaturatingCoeff(liftFit165, ReHuman165);
ClHuman180 = evalSaturatingCoeff(liftFit180, ReHuman180);

% Human drag and lift forces
DragHuman150 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman150 .* CdHuman150;
DragHuman165 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman165 .* CdHuman165;
DragHuman180 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman180 .* CdHuman180;

LiftHuman150 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman150 .* ClHuman150;
LiftHuman165 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman165 .* ClHuman165;
LiftHuman180 = 0.5 * rhoHuman .* Vhuman.^2 .* Ahuman180 .* ClHuman180;

% Plot wind speed vs drag force
figure;
plot(Vhuman, DragHuman150, 'LineWidth', 1.5);
hold on;
plot(Vhuman, DragHuman165, 'LineWidth', 1.5);
plot(Vhuman, DragHuman180, 'LineWidth', 1.5);
xlabel('Wind Speed (m/s)');
ylabel('Drag Force on Human (N)');
title('Predicted Human Drag Force vs Wind Speed');
legend('150 Degree Bend', '165 Degree Bend', '180 Degree Bend', 'Location', 'best');
grid on;

% Plot wind speed vs lift force
figure;
plot(Vhuman, LiftHuman150, 'LineWidth', 1.5);
hold on;
plot(Vhuman, LiftHuman165, 'LineWidth', 1.5);
plot(Vhuman, LiftHuman180, 'LineWidth', 1.5);
xlabel('Wind Speed (m/s)');
ylabel('Lift Force on Human (N)');
title('Predicted Human Lift Force vs Wind Speed');
legend('150 Degree Bend', '165 Degree Bend', '180 Degree Bend', 'Location', 'best');
grid on;

% Print fitted equations
fprintf('\nDrag coefficient equations: C_D = Cinf + A*exp(-Re/Re0)\n');
fprintf('150 deg: C_D = %.4f + %.4f*exp(-Re/%.4e)\n', dragFit150(1), dragFit150(2), dragFit150(3));
fprintf('165 deg: C_D = %.4f + %.4f*exp(-Re/%.4e)\n', dragFit165(1), dragFit165(2), dragFit165(3));
fprintf('180 deg: C_D = %.4f + %.4f*exp(-Re/%.4e)\n', dragFit180(1), dragFit180(2), dragFit180(3));

fprintf('\nLift coefficient equations: C_L = Cinf + A*exp(-Re/Re0)\n');
fprintf('150 deg: C_L = %.4f + %.4f*exp(-Re/%.4e)\n', liftFit150(1), liftFit150(2), liftFit150(3));
fprintf('165 deg: C_L = %.4f + %.4f*exp(-Re/%.4e)\n', liftFit165(1), liftFit165(2), liftFit165(3));
fprintf('180 deg: C_L = %.4f + %.4f*exp(-Re/%.4e)\n', liftFit180(1), liftFit180(2), liftFit180(3));


%% Local functions
function params = fitSaturatingCoeff(Re, C)
    valid = isfinite(Re) & isfinite(C) & Re > 0;
    Re = Re(valid);
    C  = C(valid);

    Cinf0 = mean(C(end-2:end));
    A0 = C(1) - Cinf0;
    Re00 = mean(Re);

    p0 = [Cinf0, A0, Re00];

    obj = @(p) sum((C - (p(1) + p(2)*exp(-Re./abs(p(3))))).^2);

    params = fminsearch(obj, p0);
    params(3) = abs(params(3));
end

function C = evalSaturatingCoeff(params, Re)
    Cinf = params(1);
    A    = params(2);
    Re0  = params(3);

    C = Cinf + A .* exp(-Re ./ Re0);
end